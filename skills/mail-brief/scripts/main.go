package main

import (
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"os/exec"
	"strings"
	"time"
)

// --- Types ---

type Account struct {
	Email string `json:"email"`
	Type  string `json:"type"`
}

type SimplifiedMessage struct {
	Date        string   `json:"date"`
	Subject     string   `json:"subject"`
	FromName    string   `json:"from_name"`
	FromEmail   string   `json:"from_email"`
	Labels      []string `json:"labels"`
	IsUnread    bool     `json:"is_unread"`
	AccountType string   `json:"account_type"`
}

type Output struct {
	Accounts []Account           `json:"accounts"`
	Messages []SimplifiedMessage `json:"messages"`
	Errors   []AccountError      `json:"errors,omitempty"`
}

type AccountError struct {
	Email string `json:"email"`
	Error string `json:"error"`
}

// --- Account Discovery & Classification ---

var personalDomains = map[string]bool{
	"gmail.com":   true,
	"naver.com":   true,
	"daum.net":    true,
	"hanmail.net": true,
	"yahoo.com":   true,
	"hotmail.com": true,
	"outlook.com": true,
	"icloud.com":  true,
	"kakao.com":   true,
	"nate.com":    true,
}

func discoverAccounts() []string {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	cmd := exec.CommandContext(ctx, "gog", "auth", "list", "--json")
	out, err := cmd.Output()
	if err != nil {
		return nil
	}

	var data struct {
		Accounts []struct {
			Email string `json:"email"`
		} `json:"accounts"`
	}
	if err := json.Unmarshal(out, &data); err != nil {
		return nil
	}

	emails := make([]string, 0, len(data.Accounts))
	for _, a := range data.Accounts {
		emails = append(emails, a.Email)
	}
	return emails
}

func classifyAccount(email string) string {
	parts := strings.SplitN(email, "@", 2)
	if len(parts) < 2 {
		return "work"
	}
	domain := strings.ToLower(parts[1])
	if personalDomains[domain] {
		return "personal"
	}
	return "work"
}

func resolveAccounts(personal, work string) []Account {
	var accounts []Account
	if personal != "" {
		accounts = append(accounts, Account{Email: personal, Type: "personal"})
	}
	if work != "" {
		accounts = append(accounts, Account{Email: work, Type: "work"})
	}
	if len(accounts) > 0 {
		return accounts
	}
	for _, email := range discoverAccounts() {
		accounts = append(accounts, Account{Email: email, Type: classifyAccount(email)})
	}
	return accounts
}

// --- Query Building ---

func buildGmailQuery(today, yesterday, thisWeek, lastWeek bool, date string) string {
	now := time.Now()

	if date != "" {
		targetDate, err := time.Parse("2006-01-02", date)
		if err == nil {
			nextDay := targetDate.AddDate(0, 0, 1)
			return fmt.Sprintf("after:%s before:%s",
				targetDate.Format("2006/01/02"),
				nextDay.Format("2006/01/02"))
		}
	}

	if lastWeek {
		weekday := now.Weekday() // Sun=0..Sat=6
		thisSunday := now.AddDate(0, 0, -int(weekday))
		lastSunday := thisSunday.AddDate(0, 0, -7)
		return fmt.Sprintf("after:%s before:%s",
			lastSunday.Format("2006/01/02"),
			thisSunday.Format("2006/01/02"))
	}

	if thisWeek {
		weekday := now.Weekday() // Sun=0..Sat=6
		thisSunday := now.AddDate(0, 0, -int(weekday))
		tomorrow := now.AddDate(0, 0, 1)
		return fmt.Sprintf("after:%s before:%s",
			thisSunday.Format("2006/01/02"),
			tomorrow.Format("2006/01/02"))
	}

	if yesterday {
		yesterdayDate := now.AddDate(0, 0, -1)
		return fmt.Sprintf("after:%s before:%s",
			yesterdayDate.Format("2006/01/02"),
			now.Format("2006/01/02"))
	}

	return "newer_than:1d"
}

// --- Message Fetching ---

func fetchMessages(accountEmail, query string) ([]map[string]interface{}, error) {
	args := []string{"gmail", "messages", "search", query, "--json", "--max=50", fmt.Sprintf("--account=%s", accountEmail)}

	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	cmd := exec.CommandContext(ctx, "gog", args...)
	var stderr strings.Builder
	cmd.Stderr = &stderr
	out, err := cmd.Output()
	if err != nil {
		errMsg := strings.TrimSpace(stderr.String())
		if errMsg == "" {
			errMsg = fmt.Sprintf("gog exited with code %d", cmd.ProcessState.ExitCode())
		}
		return nil, fmt.Errorf("%s", errMsg)
	}

	var asMap map[string]interface{}
	if err := json.Unmarshal(out, &asMap); err == nil {
		if messagesRaw, ok := asMap["messages"]; ok {
			if messagesSlice, ok := messagesRaw.([]interface{}); ok {
				return toMapSlice(messagesSlice), nil
			}
		}
		return nil, nil
	}

	var asSlice []interface{}
	if err := json.Unmarshal(out, &asSlice); err == nil {
		return toMapSlice(asSlice), nil
	}

	return nil, fmt.Errorf("unexpected JSON format from gog")
}

func toMapSlice(raw []interface{}) []map[string]interface{} {
	result := make([]map[string]interface{}, 0, len(raw))
	for _, item := range raw {
		if m, ok := item.(map[string]interface{}); ok {
			result = append(result, m)
		}
	}
	return result
}

// --- Message Processing ---

func parseFrom(raw string) (string, string) {
	raw = strings.TrimSpace(raw)
	if raw == "" {
		return "", ""
	}

	if strings.Contains(raw, "<") && strings.Contains(raw, ">") {
		parts := strings.SplitN(raw, "<", 2)
		name := strings.TrimSpace(parts[0])
		email := strings.TrimSuffix(strings.TrimPrefix(strings.TrimSpace(parts[1]), ""), ">")
		email = strings.TrimSpace(email)
		return name, email
	}

	return raw, raw
}

func getString(m map[string]interface{}, key string) string {
	if v, ok := m[key]; ok {
		if s, ok := v.(string); ok {
			return s
		}
	}
	return ""
}

func getStringSlice(m map[string]interface{}, key string) []string {
	if v, ok := m[key]; ok {
		if arr, ok := v.([]interface{}); ok {
			result := make([]string, 0, len(arr))
			for _, item := range arr {
				if s, ok := item.(string); ok {
					result = append(result, s)
				}
			}
			return result
		}
	}
	return nil
}

func simplifyMessage(msg map[string]interface{}, accountType string) SimplifiedMessage {
	subject := getString(msg, "subject")
	if subject == "" {
		subject = "(No subject)"
	}

	fromRaw := getString(msg, "from")
	fromName, fromEmail := parseFrom(fromRaw)

	labels := getStringSlice(msg, "labels")
	if labels == nil {
		labels = []string{}
	}

	// Filter out UNREAD from labels (already captured in IsUnread)
	filtered := make([]string, 0, len(labels))
	isUnread := false
	for _, label := range labels {
		if label == "UNREAD" {
			isUnread = true
		} else {
			filtered = append(filtered, label)
		}
	}

	return SimplifiedMessage{
		Date:        getString(msg, "date"),
		Subject:     subject,
		FromName:    fromName,
		FromEmail:   fromEmail,
		Labels:      filtered,
		IsUnread:    isUnread,
		AccountType: accountType,
	}
}

// --- Main ---

func main() {
	personal := flag.String("personal", "", "Personal account email")
	work := flag.String("work", "", "Work account email")
	today := flag.Bool("today", false, "Today's messages (default)")
	yesterday := flag.Bool("yesterday", false, "Yesterday's messages")
	thisWeek := flag.Bool("this-week", false, "This week (Sun-Sat)")
	lastWeek := flag.Bool("last-week", false, "Last week (Sun-Sat)")
	date := flag.String("date", "", "Specific date (YYYY-MM-DD)")
	flag.Parse()

	// Default to today when no date flag is given
	if !*today && !*yesterday && !*thisWeek && !*lastWeek && *date == "" {
		*today = true
	}

	accounts := resolveAccounts(*personal, *work)
	if len(accounts) == 0 {
		errObj := map[string]string{
			"error": "No accounts found. Use --personal/--work or configure gog auth.",
		}
		enc := json.NewEncoder(os.Stdout)
		enc.SetIndent("", "  ")
		enc.SetEscapeHTML(false)
		enc.Encode(errObj)
		os.Exit(1)
	}

	query := buildGmailQuery(*today, *yesterday, *thisWeek, *lastWeek, *date)

	var allMessages []SimplifiedMessage
	var errors []AccountError

	for _, account := range accounts {
		rawMessages, err := fetchMessages(account.Email, query)
		if err != nil {
			errors = append(errors, AccountError{Email: account.Email, Error: err.Error()})
			continue
		}
		for _, m := range rawMessages {
			allMessages = append(allMessages, simplifyMessage(m, account.Type))
		}
	}

	if allMessages == nil {
		allMessages = []SimplifiedMessage{}
	}

	output := Output{
		Accounts: accounts,
		Messages: allMessages,
	}
	if len(errors) > 0 {
		output.Errors = errors
	}

	enc := json.NewEncoder(os.Stdout)
	enc.SetIndent("", "  ")
	enc.SetEscapeHTML(false)
	enc.Encode(output)
}

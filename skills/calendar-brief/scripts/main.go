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

type SimplifiedEvent struct {
	Summary     string `json:"summary"`
	Start       string `json:"start"`
	End         string `json:"end"`
	Location    string `json:"location"`
	Status      string `json:"status"`
	Response    string `json:"response"`
	AccountType string `json:"account_type"`
}

type Output struct {
	Accounts []Account         `json:"accounts"`
	Events   []SimplifiedEvent `json:"events"`
	Errors   []AccountError    `json:"errors,omitempty"`
}

type AccountError struct {
	Email string `json:"email"`
	Error string `json:"error"`
}

// --- Account Discovery & Classification ---

var personalDomains = map[string]bool{
	"gmail.com":    true,
	"naver.com":    true,
	"daum.net":     true,
	"hanmail.net":  true,
	"yahoo.com":    true,
	"hotmail.com":  true,
	"outlook.com":  true,
	"icloud.com":   true,
	"kakao.com":    true,
	"nate.com":     true,
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

// --- Date Args ---

func buildGogArgs(today, tomorrow, thisWeek, nextWeek bool) []string {
	// Priority: next-week > this-week > tomorrow > today
	if nextWeek {
		now := time.Now()
		weekday := now.Weekday() // Sunday=0, Monday=1 ...
		// Convert to Python convention: Mon=0
		pyWeekday := (int(weekday) + 6) % 7
		daysUntilMonday := (7 - pyWeekday) % 7
		if daysUntilMonday == 0 {
			daysUntilMonday = 7
		}
		nextMonday := now.AddDate(0, 0, daysUntilMonday)
		nextSunday := nextMonday.AddDate(0, 0, 6)
		return []string{
			"--from", nextMonday.Format("2006-01-02"),
			"--to", nextSunday.Format("2006-01-02"),
		}
	}
	if thisWeek {
		return []string{"--week", "--week-start=mon"}
	}
	if tomorrow {
		return []string{"--tomorrow"}
	}
	return []string{"--today"}
}

// --- Event Fetching ---

func fetchEvents(accountEmail string, gogDateArgs []string) ([]map[string]interface{}, error) {
	args := []string{"calendar", "events", "primary", "--json", "--max=50", fmt.Sprintf("--account=%s", accountEmail)}
	args = append(args, gogDateArgs...)

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

	// Try as object with "events" key first
	var asMap map[string]interface{}
	if err := json.Unmarshal(out, &asMap); err == nil {
		if eventsRaw, ok := asMap["events"]; ok {
			if eventsSlice, ok := eventsRaw.([]interface{}); ok {
				return toMapSlice(eventsSlice), nil
			}
		}
		// dict but no "events" key — wrap it? Python returns data itself via data.get("events", data)
		// which means if "events" key missing, return the dict as-is treated as "data"
		// But since data is a dict not a list, this won't iterate well.
		// Match Python: data.get("events", data) where data is dict → returns dict
		// then `for e in raw_events` iterates over dict keys, which is unusual.
		// Practically, gog returns {"events": [...]} so this edge case is unlikely.
		// Return empty for safety.
		return nil, nil
	}

	// Try as array
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

// --- Event Processing ---

func extractMyResponse(event map[string]interface{}) string {
	attendeesRaw, ok := event["attendees"]
	if !ok {
		return ""
	}
	attendees, ok := attendeesRaw.([]interface{})
	if !ok {
		return ""
	}
	for _, aRaw := range attendees {
		a, ok := aRaw.(map[string]interface{})
		if !ok {
			continue
		}
		if selfVal, ok := a["self"]; ok {
			if isSelf, ok := selfVal.(bool); ok && isSelf {
				if rs, ok := a["responseStatus"].(string); ok {
					return rs
				}
				return ""
			}
		}
	}
	return ""
}

func getString(m map[string]interface{}, key string) string {
	if v, ok := m[key]; ok {
		if s, ok := v.(string); ok {
			return s
		}
	}
	return ""
}

func getMap(m map[string]interface{}, key string) map[string]interface{} {
	if v, ok := m[key]; ok {
		if sub, ok := v.(map[string]interface{}); ok {
			return sub
		}
	}
	return nil
}

func simplifyEvent(event map[string]interface{}, accountType string) SimplifiedEvent {
	summary := getString(event, "summary")
	if summary == "" {
		summary = "(No title)"
	}

	startMap := getMap(event, "start")
	endMap := getMap(event, "end")

	startStr := ""
	if startMap != nil {
		startStr = getString(startMap, "dateTime")
		if startStr == "" {
			startStr = getString(startMap, "date")
		}
	}

	endStr := ""
	if endMap != nil {
		endStr = getString(endMap, "dateTime")
		if endStr == "" {
			endStr = getString(endMap, "date")
		}
	}

	return SimplifiedEvent{
		Summary:     summary,
		Start:       startStr,
		End:         endStr,
		Location:    getString(event, "location"),
		Status:      getString(event, "status"),
		Response:    extractMyResponse(event),
		AccountType: accountType,
	}
}

// --- Main ---

func main() {
	personal := flag.String("personal", "", "Personal account email")
	work := flag.String("work", "", "Work account email")
	today := flag.Bool("today", false, "Today's events (default)")
	tomorrow := flag.Bool("tomorrow", false, "Tomorrow's events")
	thisWeek := flag.Bool("this-week", false, "This week (Mon-Sun)")
	nextWeek := flag.Bool("next-week", false, "Next week (Mon-Sun)")
	flag.Parse()

	// Default to today when no date flag is given
	if !*today && !*tomorrow && !*thisWeek && !*nextWeek {
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

	gogDateArgs := buildGogArgs(*today, *tomorrow, *thisWeek, *nextWeek)

	var allEvents []SimplifiedEvent
	var errors []AccountError

	for _, account := range accounts {
		rawEvents, err := fetchEvents(account.Email, gogDateArgs)
		if err != nil {
			errors = append(errors, AccountError{Email: account.Email, Error: err.Error()})
			continue
		}
		for _, e := range rawEvents {
			allEvents = append(allEvents, simplifyEvent(e, account.Type))
		}
	}

	// Ensure non-nil slices for JSON output ([] not null)
	if allEvents == nil {
		allEvents = []SimplifiedEvent{}
	}

	output := Output{
		Accounts: accounts,
		Events:   allEvents,
	}
	if len(errors) > 0 {
		output.Errors = errors
	}

	enc := json.NewEncoder(os.Stdout)
	enc.SetIndent("", "  ")
	enc.SetEscapeHTML(false)
	enc.Encode(output)
}

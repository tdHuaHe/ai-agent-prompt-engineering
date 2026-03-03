const weekday = Context.getVariable("preferred_weekday");
start_date = adjustDateToWeekday(start_date, weekday)
Context.setVariable("start_date", start_date)
const localeDate = formatDateWithOrdinal(start_date)

if(date_matched_weekday === "No"){
    Context.setVariable("workflow_status", `The date for ${weekday} should be ${localeDate}. So the correct match is:  on ${weekday}, ${localeDate}`)
}

function formatDateWithOrdinal(isoDate, locale = 'en-US') {
  const d = new Date(isoDate);
  if (Number.isNaN(d.getTime())) throw new Error('Invalid date string');

  const month = d.toLocaleString(locale, { month: 'long' });
  const day = d.getDate();

  // Ordinal suffix rules
  const suffix = (n => {
    const rem100 = n % 100;
    if (rem100 >= 11 && rem100 <= 13) return 'th';
    switch (n % 10) {
      case 1: return 'st';
      case 2: return 'nd';
      case 3: return 'rd';
      default: return 'th';
    }
  })(day);

  return `${month} ${day}${suffix}`;
}

/**
 * Adjust start_date to match the preferred weekday
 * @param {string} startDate - The starting date (YYYY-MM-DD format)
 * @param {string} weekday - The preferred weekday (e.g., 'monday', 'tue')
 * @returns {object} Object with adjustedDate and matchedWeekday flag
 */
function adjustDateToWeekday(startDate, weekday) {
    let adjustedDate = startDate;
    
    if (adjustedDate === null || adjustedDate === "") {
        adjustedDate = new Date().toISOString().split('T')[0];
    }
    
    // Adjust date to match preferred weekday if provided
    if (weekday && weekday !== "" && weekday !== null) {
        const targetDate = new Date(adjustedDate);
        const weekdayMap = {
            'sunday': 0, 'sun': 0,
            'monday': 1, 'mon': 1,
            'tuesday': 2, 'tue': 2,
            'wednesday': 3, 'wed': 3,
            'thursday': 4, 'thu': 4,
            'friday': 5, 'fri': 5,
            'saturday': 6, 'sat': 6
        };
        
        const targetWeekday = weekdayMap[weekday.toLowerCase()];
        
        if (targetWeekday !== undefined) {
            const currentWeekday = targetDate.getDay();
            
            // If current day doesn't match preferred weekday, find next occurrence
            if (currentWeekday !== targetWeekday) {
                date_matched_weekday = "No"
                original_start_date = adjustedDate
                let daysToAdd = targetWeekday - currentWeekday;
                
                // Find the closest occurrence (could be previous or next week)
                // If difference is more than 3 days, go to the other direction
                if (daysToAdd > 3) {
                    daysToAdd -= 7; // Go to previous week instead
                } else if (daysToAdd < -3) {
                    daysToAdd += 7; // Go to next week instead
                }
                targetDate.setDate(targetDate.getDate() + daysToAdd);
                adjustedDate = targetDate.toISOString().split('T')[0];
            }
        }
    }
    
    return adjustedDate;
}
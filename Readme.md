# 🌞 NoGlassesClasses - A SunSmart Scheduler  

Optimizing outdoor and indoor school activities using local sunlight data to promote **student health, vision, and productivity**.  

---

## 📌 Problem Statement  

Excessive sun exposure during school hours can increase the risk of UV-related health issues (e.g., sunburn, heat stress).  
At the same time, **insufficient outdoor activity contributes to rising cases of childhood myopia (nearsightedness)** and negatively impacts physical and mental wellbeing.  

Schools need a balanced schedule that:  
- Maximizes safe outdoor learning opportunities  
- Prevents overexposure to peak sun hours  
- Supports eye health and reduces the risk of myopia progression  

---

## 💡 Our Solution  

The **SunSmart Scheduler** dynamically generates a monthly class timetable for grades 1–5:  

- Uses **astronomical sunrise/sunset data** for a given location  
- Ensures **2 outdoor classes per day**, avoiding peak UV hours  
- Distributes indoor classes fairly across remaining time slots  
- Exports schedules in **CSV format** for easy sharing with teachers & parents  

---
## 🎯 Motivation
  - Rising Childhood Myopia:
      description: >
        Studies suggest that limited outdoor exposure is a major factor in the global increase 
        of myopia among children. Outdoor light stimulates healthy eye growth and can slow 
        down myopia progression.

  - Health & Safety Balance:
      description: >
        Schools often struggle to balance outdoor learning with UV safety. While outdoor 
        time is essential, unplanned exposure during peak UV hours raises health risks.

  - Tech for Social Good:
      description: >
        Our motivation is to empower schools with data-driven schedules that not only promote 
        eye health but also ensure overall student wellbeing through optimized learning environments.

## 📚 Research References
  - title: "The Impact of Myopia and High Myopia"
    organization: "World Health Organization (WHO)"
    key_finding: "Outdoor time reduces the risk of myopia onset and progression in children."
    year: 2019
    link: "https://www.who.int/publications/i/item/9789241516570"

  - title: "Childhood Myopia"
    organization: "American Academy of Ophthalmology (AAO)"
    key_finding: "Spending more time outdoors lowers the chances of becoming myopic."
    year: 2020
    link: "https://www.aao.org/eye-health/diseases/myopia-childhood-nearsightedness"

  - title: "SunSmart Guidelines for Schools"
    organization: "Cancer Council Australia"
    key_finding: "Schools should schedule outdoor activities to minimize time in peak UV radiation periods."
    link: "https://www.sunsmart.com.au/schools"


---
## 🛠️ Tech Stack  

- **Python 3.9+**  
- **Astral** → Sunrise/Sunset & daylight calculation  
- **pytz** → Timezone support  
- **requests** → Location → Coordinates lookup  
- **timezonefinderL** → Auto-detect timezone (optional)  

---

## ⚙️ Installation  

Clone the repo and install dependencies:  

```bash
Enter your school city: Amritsar
Enter your country: India
Enter timezone (e.g., Asia/Kolkata): Asia/Kolkata
Enter month (1-12): 6
Enter grades (e.g., 1-5, 8, 10-12): 3
Enter number of classes per day: 7
Enter class length in minutes: 40
Max consecutive outdoor classes allowed: 3
Enter number of sections in Grade 3: 2
Do you want schedule for a Day, Week (5 days), or Week (6 days)? 1

🌞 Avg daylight hours in Amritsar, India (June): 13.47 hrs

📅 Final Timetable:

===== Day 1 =====
Grade 3 - Section 1:
  Class 1: Outdoor
  Class 2: Outdoor
  Class 3: Indoor
  Class 4: Indoor
  Class 5: Outdoor
  Class 6: Indoor
  Class 7: Indoor

Grade 3 - Section 2:
  Class 1: Indoor
  Class 2: Outdoor
  Class 3: Outdoor
  Class 4: Indoor
  Class 5: Outdoor
  Class 6: Indoor
  Class 7: Indoor


Do you want to save this schedule as a CSV file? (yes/no): yes

✅ Schedule saved to schedule_June.csv
```
## ✨ Features
✅ Location-based sunrise/sunset calculation
✅ Balances outdoor vs indoor activities
✅ Encourages outdoor time → reduces childhood myopia risk
✅ Exports schedules to CSV for record-keeping
✅ Emoji-enhanced console output for readability

## 🚀 Future Improvements
🌤️ Integrate real-time UV index APIs for more accurate risk assessment
📱 Build a mobile/web dashboard for school admins
🧠 Add machine learning to adapt schedules using weather/attendance data
👓 Track myopia prevalence trends to validate long-term health benefits



## 👩‍💻 Author
Supreet Kaur
📧 supreetkaur0602@gmail.com

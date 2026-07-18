# pullela_court_watcher
This project watches the opening of slots in gopichand academy site

How this is going to work:
1. We are directly reading from the API that the website calls when we open the page
2.  i. The URL has two parts - 
        a. path : https://adminbooking.gopichandacademy.com/API/Get/Calender
        b. query string : venue_id=3&date=2026-07-18
        The `venue_id` and `date` are the parameters here. 
   ii. It returns the json file in the sample format:
   ```json
   {
    "Status": "Success",
    "Message": "Data found successfully.",
    "Result": {
        "25": {
            "id": "41",
            "court_id": "25",
            "court_name": "1",
            "court_type": "Indoor",
            "court_charges": "405",
            "court_all_slots": [
                "11:00-12:00|1",
                "12:00-13:00|1",
                "13:00-14:00|1",
                "14:00-15:00|1",
                "15:00-16:00|1",
                "16:00-17:00|1",
                "17:00-18:00|1",
                "18:00-19:00|1",
                "19:00-20:00|1",
                "20:00-21:00|1",
                "21:00-22:00|1"
            ],
            "court_booked_slots": [
                "11:00-12:00|1",
                "12:00-13:00|1",
                "13:00-14:00|1",
                "14:00-15:00|1",
                "15:00-16:00|1",
                "16:00-17:00|1",
                "17:00-18:00|1",
                "18:00-19:00|1",
                "19:00-20:00|1",
                "20:00-21:00|1",
                "21:00-22:00|1"
            ],
            "court_available_slots": [
                "11:00-12:00|0|405",
                "12:00-13:00|0|405",
                "13:00-14:00|0|405",
                "14:00-15:00|0|405",
                "15:00-16:00|0|405",
                "16:00-17:00|0|405",
                "17:00-18:00|0|405",
                "18:00-19:00|0|405",
                "19:00-20:00|0|405",
                "20:00-21:00|0|405",
                "21:00-22:00|0|405"
            ]
        },
        "26": {
            "id": "42",
            "court_id": "26",
            "court_name": "2",
            "court_type": "Indoor",
            "court_charges": "405",
            "court_all_slots": [
                "11:00-12:00|1",
                "12:00-13:00|1",
                "14:00-15:00|1",
                "16:00-17:00|1",
                "17:00-18:00|1",
                "18:00-19:00|1",
                "19:00-20:00|1",
                "20:00-21:00|1",
                "21:00-22:00|1"
            ],
            "court_booked_slots": [
                "11:00-12:00|1",
                "12:00-13:00|1",
                "14:00-15:00|1",
                "16:00-17:00|1",
                "17:00-18:00|1",
                "18:00-19:00|1",
                "19:00-20:00|1",
                "20:00-21:00|1",
                "21:00-22:00|1"
            ],
            "court_available_slots": [
                "11:00-12:00|0|405",
                "12:00-13:00|0|405",
                "14:00-15:00|0|405",
                "16:00-17:00|0|405",
                "17:00-18:00|0|405",
                "18:00-19:00|0|405",
                "19:00-20:00|0|405",
                "20:00-21:00|0|405",
                "21:00-22:00|0|405"
            ]
        }
       }
    }
   ```
3. The logic to check whether slots are open or not is simple. We just check whether value of court_all_slots/court_booked_slots/court_available_slots are empty or not. We could've gone for more definitive and rigorous logic by checking one of the court_available_slots is non-zero.
4. If the slots were open, we send a message to my telegram using a bot. This bot was created using botfather.
   i. The botfather generates a `BOT_TOKEN` for HTTP API. We will know the `CHAT_ID` once we access the API. 
   ii. The `BOT_TOKEN` and `CHAT_ID` were masked using *secrets* feature in github.

Few more ideas:
1. I will look to make this more complete project by looking to automate till payment.
2. Instead of telegram message, we could try sending a mail.


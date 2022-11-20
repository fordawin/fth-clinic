function getBotResponse(input) {
    //rock paper scissors
    if (input.match("services") || input.match("Services") || input.match("Service") || input.match("service")) {
        return "Our medical center offers: <br>- Massage<br>- Acupuncture<br>- Checkups";
    } else if (input.match("specialize") || input.match("Specialize") || input.match("Specialization") || input.match("specialization")) {
        return "Our medical center specializes in: - Asthma & Emphysema <br> - Bladder Stones <br> - Cancer <br> - Diabetes <br> - Dysmenorrhea <br> - Eye & Skin Disease <br> - Gallstones <br> - Hemorrhoids <br> - Hypertension <br> - Impotence <br> - Infertility <br> - Insomnia <br> - Kidney Stones <br> -  Migraine  <br> - Neurasthenia <br> - Obesity <br> - Parkinson’s Disease <br> - Prostatitis <br> - Rheumatism Arthritis <br> - Sinusitis"; 
    } else if (input.match("emergency") || input.match("Emergency") || input.match("emergencies") || input.match("Emergencies")) {
        return "Sorry, we only offer specific services.";
    } else if (input.match("walk-in") || input.match("walk-ins") || input.match("walk in") || input.match("walk ins")) {
        return "Yes, but it should be within operating hours.";
    } else if (input.match("located") || input.match("Located") || input.match("Location") || input.match("location") || input.match("Place") || input.match("place")) {
        return "Unit 5 24K Mansion, 45 Timog Ave corner Sct Tuason St., South Triangle, QC. Located opposite Shell gasoline station. You can also find 'Faith Hope Love Medical Center' in Waze!";
    } else if (input.match("Facebook") || input.match("facebook") || input.match("fb") || input.match("FB")  || input.match("Fb")) {
        return "www.facebook.com/faithhopelove<br>medicalcenter/";
    } else if (input.match("operating hours") || input.match("opening") || input.match("closing") || input.match("Opening") || input.match("Closing")) {
        return "Clinic hours are 9am to 12nn and 2pm to 6pm, Mondays to Saturdays";
    } else if (input.match("contact") || input.match("Contact") || input.match("contacts") || input.match("Contact information") || input.match("contact information") || input.match("Contact informations") || input.match("contact informations")) {
        return "You may reach us through these contacts: <br><b>Landline:</b><br> - 83734418 <br> - 77386131 <br><b>Cellphone:</b><br> - <b>SMART</b> : 83734418 <br> - <b>GLOBE</b> : 77386131";
    } else if (input.match("how much") || input.match("How much") || input.match("Price") || input.match("price") || input.match("costs") || input.match("cost") || input.match("Costs") || input.match("Cost")) {
        return "Prices vary depending on the desired service.";
    } else if (input.match("payments") || input.match("payment") || input.match("Payment") || input.match("Payments") || input.match("mop") || input.match("MOP")) {
        return "For buying our products: <br> Face to face payment, the system will provide you an invoice statement. <br> For booking an appointment: <br> Face to face payment, the system will provide you an invoice statement.";
    } else if (input.match("appointment details") || input.match("details of appointment") || input.match("appointment information") || input.match("information of appointment") || input.match("Appointment details") || input.match("Details of appointment") || input.match("Appointment information") || input.match("Information of appointment")) {
        return "Your appointment details will show  up on your profile once you have successfully booked an appointment.";
    }
    // Simple responses
    if (input == "hello") {
        return "Hello there!";
    } else if (input == "goodbye") {
        return "Talk to you later!";
    } else {
        return "Try asking something else!";
    }
}
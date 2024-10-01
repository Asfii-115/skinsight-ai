from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.contrib.auth import logout
from .models import UserProfile, UploadedImage
from .forms import UploadImageForm
from .models import UploadedImage
from .image_classifier import preprocess_and_predict  # Import the preprocess_and_predict function
from .models import PaymentRequest
from django.http import JsonResponse
from .forms import UserProfileForm


def result_details(request, disease):
    # Define a dictionary that maps diseases to their corresponding paragraphs
    disease_paragraphs = {
    "['Melanoma']": """
        Melanoma is a serious form of skin cancer that can be life-threatening if not detected and treated early. Here are some general guidelines for managing melanoma:

                    <p>1. Consult a Dermatologist or Oncologist: If you suspect you have melanoma or if you notice any changes in your 
                        moles or skin, it's crucial to consult a dermatologist or oncologist promptly. 
                        Early detection and treatment are essential for a better prognosis.</p>
                    
                    <p>2. Sun Protection: Protect your skin from harmful UV radiation. Use broad-spectrum sunscreen with SPF 30 or 
                        higher, wear protective clothing (long sleeves, wide-brimmed hats, sunglasses), 
                        and seek shade, especially during peak sun hours.</p>
                    
                    <p>3. Regular Skin Examinations: Perform regular self-examinations of your skin, including moles, to check 
                    for changes in size, shape, color, or any new growths. You can use the ABCDE rule as a guide for identifying 
                    suspicious moles: Asymmetry, Border irregularity, Color variation, Diameter larger than a pencil eraser, 
                    and Evolving or changing characteristics.</p>
                    
                    <p>4. Avoid Tanning Beds: Tanning beds and lamps emit UV radiation that can increase your risk of melanoma. 
                    Avoid using them.</p>
                    
                    <p>5. Seek Professional Skin Checks: Have regular skin checks by a dermatologist, especially 
                        if you have a family history of melanoma or other risk factors.
                    </p>
                    <p>6. Protect Your Eyes: Wear sunglasses that provide 100% UV protection to shield your 
                        eyes from harmful UV rays.
                    </p>
                    
                    
                    <p>7. Lymph Node Evaluation: In cases where melanoma has spread, lymph node evaluation 
                        may be necessary to determine the extent of the disease and guide treatment decisions.
                    </p>
                    
                    <p>8. Lifestyle Factors: Maintain a healthy lifestyle by eating a balanced diet, staying 
                        physically active, and avoiding smoking and excessive alcohol consumption. A healthy 
                        lifestyle can support your overall well-being during and after cancer treatment.
                    </p>
                    
                    <p>9. Clinical Trials: Discuss with your oncologist whether participating in clinical 
                        trials is an option. Clinical trials can provide access to innovative treatments and therapies.
                    </p>
                    <p>Remember that melanoma is a complex and potentially aggressive cancer, so early detection and timely 
                    treatment are crucial for improving outcomes. Regular skin checks and sun protection are essential 
                    steps in melanoma management and prevention. Always consult with healthcare professionals for 
                    personalized advice and treatment options.
        """,
            "['Atopic Dermatitis']": """
        Atopic typically refers to a group of allergic conditions, including atopic dermatitis (eczema), 
                    allergic rhinitis (hay fever), and asthma, which are often linked by an underlying tendency to 
                    develop allergies. Here are some general suggestions for managing atopic conditions:

                    <p>1. Consult an Allergist or Immunologist: If you suspect you have atopic conditions or if you've 
                    been diagnosed with one, it's important to consult an allergist or immunologist. 
                    They can help identify specific triggers and develop a comprehensive treatment plan.</p>

                    <p>2. Identify and Avoid Triggers: Work with your healthcare provider to identify and avoid allergens
                    or irritants that trigger your atopic symptoms. Common triggers may include pollen, dust mites, 
                    pet dander, certain foods, or specific environmental factors.</p>

                    <p>3. Medication Management: Depending on the type of atopic condition you have, your healthcare provider 
                    may recommend medications. These can include antihistamines, corticosteroids, bronchodilators, or other
                    allergy medications. Always follow your healthcare provider's instructions regarding medication use.</p>

                    <p>4. Allergen Immunotherapy: In some cases, allergen immunotherapy, such as allergy shots or sublingual 
                    tablets, may be recommended to desensitize your immune system to specific allergens.</p>

                    <p>5. Skin Care for Atopic Dermatitis (Eczema): If you have atopic dermatitis, follow the eczema
                    management suggestions provided earlier in this conversation.</p>

                    <p>6. Asthma Management: If you have asthma, follow your asthma action plan, which typically 
                    includes using inhalers as prescribed, avoiding asthma triggers, and seeking immediate 
                    medical attention during asthma attacks.</p>

                    <p>7. Nasal Allergy Management: For allergic rhinitis (hay fever), consider saline nasal irrigation, 
                    using air purifiers, and discussing appropriate nasal sprays or antihistamines with your 
                    healthcare provider.</p>

                    <p>8. Dietary Considerations: If you have food allergies as part of your atopic conditions, work with 
                    a healthcare provider or allergist to develop a safe and balanced diet plan. They can help you 
                    identify and manage food allergens.</p>

                    <p>9. Environmental Modifications: Make necessary modifications to your home environment to reduce 
                    exposure to allergens. This may include using allergen-proof covers for pillows and mattresses, 
                    regularly cleaning and vacuuming, and maintaining a clean and allergen-free sleeping area.</p>


                    <p>10. Regular Check-Ups: Attend regular follow-up appointments with your healthcare 
                    provider to monitor your condition and adjust your treatment plan as needed.</p>

                    <p>11. Lifestyle Modifications: Maintain a healthy lifestyle by staying physically 
                        active, eating a balanced diet, managing stress, and avoiding smoking or excessive 
                        alcohol consumption. These lifestyle factors can help support your overall health and well-being.</p>



                    <p>Remember that atopic conditions can vary widely from person to person, so it's important 
                        to work closely with healthcare professionals to develop a personalized management plan 
                        tailored to your specific needs and triggers.</p>
        """,
            "['Basal Cell Carcinoma']": """
        Basal cell carcinoma (BCC) is a type of skin cancer that typically develops on sun-exposed areas 
                        of the body, such as the face, ears, neck, and scalp. While it is generally slow-growing and 
                        rarely spreads to other parts of the body, early detection and appropriate management are essential. 
                        Here are some general suggestions for managing basal cell carcinoma:</p>
                        
                        <p>1. Consult a Dermatologist or Oncologist: If you suspect you have basal cell carcinoma or have 
                        been diagnosed with it, consult a dermatologist or oncologist specializing in skin cancer. 
                        They can provide a proper diagnosis and treatment plan tailored to your specific situation.</p>
                        
                        <p>2. Sun Protection: Protect your skin from UV radiation. Use broad-spectrum sunscreen with 
                        SPF 30 or higher, wear protective clothing, including wide-brimmed hats and sunglasses, 
                        and seek shade, especially during peak sun hours.</p>
                        
                        <p>3. Regular Skin Examinations: Perform regular self-examinations of your skin to check 
                        for changes in existing moles or the appearance of new growths. Early detection is key.</p>
                        
                        <p>4. Avoid Tanning Beds: Avoid using tanning beds and lamps, as they emit harmful UV 
                        radiation that can increase your risk of skin cancer.</p>
                        
                        <p>5. Medical Treatment: The primary treatment for basal cell carcinoma is usually surgical 
                        removal. This can include procedures such as excision, Mohs surgery, or electrodesiccation 
                        and curettage (ED&C). Your healthcare provider will determine the most appropriate treatment 
                        based on the size, location, and type of the lesion.</p>
                        
                        <p>6. Preservation of Healthy Tissue: Procedures like Mohs surgery aim to remove the cancerous
                         tissue while preserving as much healthy tissue as possible. Discuss surgical options and their
                         implications with your healthcare provider.</p>
                        
                        <p>7. Topical Medications: For certain cases of superficial basal cell carcinoma or those not 
                        suitable for surgery, topical medications like imiquimod or 5-fluorouracil may be prescribed.</p>
                        
                        <p>8. Follow-Up Appointments: Attend regular follow-up appointments with your healthcare provider 
                        to monitor your condition, check for recurrences, and address any concerns.</p>
                        
                        <p>9. Lifestyle Factors: Maintain a healthy lifestyle by eating a balanced diet, staying physically 
                        active, managing stress, and avoiding smoking and excessive alcohol consumption. A healthy lifestyle
                         can support your overall well-being during and after cancer treatment.</p>
                        
                        
                        <p>10. Skin Protection After Treatment: After surgical removal or treatment, take extra care to protect
                         your skin from the sun to prevent further skin cancers and minimize the risk of recurrence.</p>
                        
                        <p>11. Clinical Trials: Discuss with your healthcare provider whether participating in clinical trials 
                        for skin cancer is an option. Clinical trials can provide access to innovative treatments and therapies.</p>
                        
                        <p>It's important to remember that basal cell carcinoma is generally highly treatable, especially when 
                        detected early. Regular skin examinations, sun protection, and seeking prompt medical attention are 
                        crucial steps in managing and preventing this type of skin cancer. Always consult with healthcare 
                        professionals for personalized advice and treatment options.</p>
        """,
            "['Eczema']": """
        <p>Eczema is a common skin condition characterized by red, itchy, and inflamed patches of skin. 
                    It can be chronic and may require ongoing management to keep symptoms under control. Here 
                    are some general guidelines for managing eczema:</p>

                    <p>1. Consult a Dermatologist: If you suspect you have eczema or if you have been diagnosed 
                    with it, it's essential to consult a dermatologist for a proper diagnosis and treatment 
                    plan. They can help determine the type of eczema you have and recommend appropriate treatments.</p>

                    <p>2. Keep Skin Moisturized: Moisturizing is a crucial part of eczema management. Use a 
                    good-quality, fragrance-free moisturizer regularly, especially after bathing. This 
                    helps to lock in moisture and prevent dryness, which can exacerbate eczema symptoms.</p>

                    <p>3. Avoid Triggers: Identify and avoid triggers that can worsen your eczema symptoms. 
                    Common triggers include certain fabrics (like wool), soaps, detergents, fragrances, 
                    and environmental factors like extreme temperatures. Try to stay in a climate-controlled 
                    environment when possible.</p>

                    <p>4. Gentle Cleansing: Use a mild, fragrance-free soap or cleanser when bathing, and avoid 
                    hot water, as it can further dry out your skin. Take shorter, lukewarm showers or baths.</p>

                    <p>5. Pat Dry, Don't Rub: After bathing or washing your hands, pat your skin dry gently with 

                    a soft towel. Avoid rubbing, which can irritate the skin.</p>

                    <p>6. Prescription Medications: Depending on the severity of your eczema, your dermatologist 
                    may prescribe topical corticosteroids or other medications to help manage inflammation and itching.</p>

                    <p>7. Topical Calcineurin Inhibitors: In some cases, non-steroidal creams like tacrolimus or 
                    pimecrolimus may be recommended to manage eczema symptoms.</p>

                    <p>8. Oral Medications: For severe cases, oral medications like antihistamines or systemic
                    corticosteroids may be prescribed for short-term relief.</p>

                    <p>9. Wet Wrap Therapy: In severe cases, wet wrap therapy can be employed under the guidance 
                    of a healthcare professional. This involves applying a moisturizer and wet bandages to the 
                    affected areas to provide relief.</p>

                    <p>10. Manage Stress: Stress can exacerbate eczema symptoms. Practice stress-reduction techniques
                    such as meditation, yoga, or deep breathing exercises.</p>

                    <p>11. Dietary Considerations: Some people find that certain foods can trigger their eczema. 
                    Keeping a food diary and working with a healthcare provider can help identify and manage dietary triggers.</p>

                    <p>12. Avoid Scratching: Scratching can make eczema worse and lead to skin infections. Keep your nails
                    short and consider wearing cotton gloves at night to prevent scratching while you sleep.</p>

                    <p>13. Allergen Avoidance: If allergies contribute to your eczema, take steps to minimize exposure 
                    to allergens. This may include using allergen-proof covers on pillows and mattresses or using an air purifier.</p>

                    <p>14. Hydration: Drink plenty of water to keep your skin hydrated from the inside out.</p>


                    <p>Remember that eczema varies from person to person, and what works for one individual may not 
                    work for another. It's essential to work closely with a healthcare professional to develop a 
                    personalized eczema management plan tailored to your specific needs.</p>
        """,
            "['Melanocytic Nevi']": """
        <p>Melanocytic nevi, commonly referred to as moles, are benign (non-cancerous) skin growths that 
                        can appear in various shapes, sizes, and colors. While most moles are harmless, it's essential 
                        to monitor them for changes and be aware of any potential warning signs. Here are some general 
                        suggestions for managing melanocytic nevi:</p>
                        
                        <p>1. Skin Self-Examinations: Perform regular self-examinations of your skin to monitor existing 
                        moles and identify any changes in size, shape, color, or texture. Pay attention to the ABCDE criteria:
                        
                        A: Asymmetry (one half of the mole does not match the other)
                        B: Border irregularity (the edges are not smooth or uniform)
                        C: Color variation (uneven coloring or multiple colors within the mole)
                        D: Diameter larger than a pencil eraser (about 6 mm or ¼ inch)
                        E: Evolution or changing characteristics (any evolving or new symptoms)</p>
                        
                        <p>2. Full-Body Skin Checks: Consider having full-body skin checks performed by a dermatologist, 
                        especially if you have a large number of moles, a family history of melanoma, or other risk factors.</p>
                        
                        <p>3. Sun Protection: Protect your skin from UV radiation by using broad-spectrum sunscreen with SPF 30 
                        or higher, wearing protective clothing (hats, long sleeves, sunglasses), and seeking shade, especially
                        during peak sun hours.</p>
                        
                        <p>4. Avoid Tanning Beds: Avoid the use of tanning beds and lamps, as UV radiation from artificial
                         sources can increase the risk of skin damage and potentially cancerous changes in moles.</p>
                        
                        <p>5. Consult a Dermatologist: If you notice any suspicious changes in your moles or if you have
                         concerns about a particular mole, consult a dermatologist for a professional evaluation.</p>
                        
                        <p>6. Biopsy or Removal: If your dermatologist believes that a mole should be further evaluated, 
                        they may recommend a biopsy or removal. This involves taking a small sample of the mole tissue
                         for examination by a pathologist.</p>
                        
                        <p>7. Skin Care: Keep your skin healthy and moisturized to prevent dryness and irritation, which
                         can lead to discomfort or changes in moles.</p>
                        
                        <p>8. Lifestyle Factors: Maintain a healthy lifestyle by eating a balanced diet, staying physically
                         active, managing stress, and avoiding smoking and excessive alcohol consumption. These factors 
                        can support overall skin health.</p>
                        
                        
                        <p>It's important to note that the vast majority of moles are harmless, but it's essential to be 
                        vigilant about changes in your skin and to consult a dermatologist if you notice any suspicious
                        alterations in your moles. Early detection and prompt medical attention can be crucial for 
                        identifying potential issues and ensuring proper management. Always consult with healthcare 
                        professionals for personalized advice and evaluation of your moles.</p>
        """
        # Add more diseases and their corresponding paragraphs as needed
        }

    # Retrieve the corresponding paragraph for the given disease name
    paragraph = disease_paragraphs.get(disease, "Paragraph not found for this disease.")

    # Pass the paragraph to the template for rendering
    return render(request, 'result_details.html', {'disease': disease, 'paragraph': paragraph})
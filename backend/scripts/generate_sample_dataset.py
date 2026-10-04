import json
import random
import os
import sys
from pathlib import Path

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.config import RAW_CORPUS_PATH

# 17 Topics and Multi-lingual Sentence Templates
TOPICS = [
    "Computer Science", "Artificial Intelligence", "Machine Learning", "India",
    "Telangana", "Andhra Pradesh", "Hyderabad", "Mathematics", "Physics",
    "Engineering", "Technology", "History", "Geography", "Education",
    "Medicine", "Agriculture", "Environment"
]

TELUGU_TEMPLATES = [
    "{topic} అనేది ఆధునిక సమాజంలో ప్రముఖ పాత్ర పోషిస్తున్న శాస్త్రం. కంప్యూటర్ మరియు సాంకేతిక పరిజ్ఞానం పెరుగుతున్న క్రమంలో కృత్రిమ మేధస్సు ప్రాముఖ్యత సంతరించుకుంది. {extra}",
    "హైదరాబాద్ నగరం మరియు తెలంగాణ రాష్ట్రం ఐటీ పరిశ్రమలో వేగంగా పురోగమిస్తున్నాయి. కంప్యూటర్ సైన్స్ మరియు డేటా విశ్లేషణ రంగాలలో అనేక పరిశోధనలు జరుగుతున్నాయి. {extra}",
    "ఆంధ్రప్రదేశ్ మరియు తెలంగాణ ప్రాంతాలలో విద్యా సంస్థలు కంప్యూటర్ భాషలు, యంత్ర అభ్యాసనం మరియు ఇంజనీరింగ్ విభాగాలకు ప్రాధాన్యత ఇస్తున్నాయి. {extra}",
    "కంప్యూటర్ ప్రోగ్రామింగ్, డేటా స్ట్రక్చర్స్ మరియు అల్గారిథమ్స్ ఇన్వర్టెడ్ ఇండెక్స్ సెర్చ్ ఇంజిన్ రూపకల్పనలో సహాయపడతాయి. {extra}",
    "భారతదేశం విజ్ఞాన మరియు సాంకేతిక రంగాలలో ప్రపంచ ప్రసిద్ధి చెందింది. గణితం, భౌతిక శాస్త్రం మరియు వ్యవసాయ రంగాలు అభివృద్ధి చెందుతున్నాయి. {extra}",
    "కృత్రిమ మేధస్సు (AI) మరియు మెషిన్ లెర్నింగ్ (ML) ద్వారా డేటా విశ్లేషణ మరియు శోధన ప్రక్రియ వేగవంతం అవుతుంది. {extra}",
    "పర్యావరణ పరిరక్షణ, వ్యవసాయ అభివృద్ధి మరియు వైద్య రంగాలలో నూతన సాంకేతికతలు ఉపయోగించబడుతున్నాయి. {extra}",
    "చరిత్ర మరియు భూగోళశాస్త్రం భారతదేశ వైవిధ్యాన్ని వివరిస్తాయి. భాషా విశ్లేషణ మరియు యూనికోడ్ ప్రాసెసింగ్ ఇండెక్సింగ్ సెర్చ్‌లో ముఖ్యం. {extra}"
]

TELUGU_EXTRAS = [
    "ఈ సమాచారం విజ్ఞాన వ్యాప్తికి తోడ్పడుతుంది.",
    "సమాచార పునరుద్ధరణ (Information Retrieval) వ్యవస్థలు డేటాను వేగంగా వెతకడానికి ఇండెక్స్ ఉపయోగిస్తాయి.",
    "తెలుగు భాషలోని విజ్ఞాన సర్వస్వం వికీపీడియా ద్వారా అందుబాటులోకి వస్తోంది.",
    "సాంకేతిక పరిజ్ఞానంతో విద్యార్థులు నూతన ఆవిష్కరణలు చేస్తున్నారు.",
    "డేటాబేస్ మరియు అల్గారిథమ్స్ సెర్చ్ ఇంజిన్ సామర్థ్యాన్ని పెంచుతాయి."
]

HINDI_TEMPLATES = [
    "{topic} भारत में एक महत्वपूर्ण विषय है। कंप्यूटर विज्ञान और प्रौद्योगिकी के क्षेत्र में तेजी से विकास हो रहा है। {extra}",
    "कृत्रिम बुद्धिमत्ता (AI) और मशीन लर्निंग आधुनिक खोज इंजन और डेटा विश्लेषण की नींव हैं। {extra}",
    "हैदराबाद और तेलंगाना सूचना प्रौद्योगिकी और इंजीनियरिंग शिक्षा के प्रमुख केंद्र हैं। {extra}"
]

HINDI_EXTRAS = [
    "यह भारतीय भाषाओं में ज्ञान का विस्तार करता है।",
    "यूनिकोड और डेटा संरचनाएं आधुनिक खोज प्रणालियों को सशक्त बनाती हैं।"
]

TAMIL_TEMPLATES = [
    "{topic} என்பது ஒரு முக்கிய துறையாகும். கணினி அறிவியல் மற்றும் தொழில்நுட்பம் இந்தியாவில் வேகமாக വളர்கிறது. {extra}",
    "செயற்கை நுண்ணறிவு மற்றும் தரவு பகுப்பாய்வு மூலம் தேடல் பொறி செயல்படுகிறது. {extra}"
]
TAMIL_EXTRAS = ["தமிழ் மொழியில் தகவல் தொழில்நுட்ப கருத்துக்கள் வளர்கின்றன."]

KANNADA_TEMPLATES = [
    "{topic} ವಿಷಯವು ಆಧುನಿಕ ಕಾಲದಲ್ಲಿ ಪ್ರಮುಖವಾಗಿದೆ. ಗಣಕಯಂತ್ರ ವಿಜ್ಞಾನ ಮತ್ತು ತಂತ್ರಜ್ಞಾನ ಅಭಿವೃದ್ಧಿಯಾಗುತ್ತಿದೆ. {extra}",
    "ಕೃತಕ ಬುದ್ಧಿಮತ್ತೆ ಮತ್ತು ಡೇಟಾ ವಿಶ್ಲೇಷಣೆ ಹುಡುಕಾಟ ಇಂಜಿನ್ ಕಾರ್ಯಕ್ಕೆ ನೆರವಾಗುತ್ತದೆ. {extra}"
]
KANNADA_EXTRAS = ["ಕನ್ನಡ ಭಾಷೆಯಲ್ಲಿ ಉನ್ನತ ತಂತ್ರಜ್ಞಾನ ಲೇಖನಗಳು ಲಭ್ಯವಿವೆ."]

MALAYALAM_TEMPLATES = [
    "{topic} എന്നത് പ്രധാനപ്പെട്ട വിഷയമാണ്. കമ്പ്യൂട്ടർ സയൻസും കൃത്രിമ ബുദ്ധിശക്തിയും സാങ്കേതിക മുന്നേറ്റം ഉണ്ടാക്കുന്നു. {extra}"
]
MALAYALAM_EXTRAS = ["മലയാളം വിക്കിപീഡിയ വിവരശേഖരണത്തിന് ഉപയോഗപ്രദമാണ്."]

BENGALI_TEMPLATES = [
    "{topic} ভারতের একটি অত্যন্ত গুরুত্বপূর্ণ বিষয়। কম্পিউটার বিজ্ঞান ও কৃত্রিম বুদ্ধিমত্তা গবেষণায় নতুন দিগন্ত উন্মোচন করছে। {extra}"
]
BENGALI_EXTRAS = ["বাংলা ভাষায় প্রযুক্তিগত তথ্য অনুসন্ধান সহজ হচ্ছে।"]

MARATHI_TEMPLATES = [
    "{topic} हे क्षेत्र आधुनिक तंत्रज्ञानात महत्त्वाचे आहे. संगणक शास्त्र आणि डेटा विश्लेषण वेगाने विकसित होत आहे. {extra}"
]
MARATHI_EXTRAS = ["मराठी भाषेतील ज्ञानकोश माहिती शोधण्यासाठी उपयुक्त आहे."]

PUNJABI_TEMPLATES = [
    "{topic} ਇੱਕ ਮਹੱਤਵਪੂਰਨ ਖੇਤਰ ਹੈ। ਕੰਪਿਊਟਰ ਵਿਗਿਆਨ ਅਤੇ ਤਕਨਾਲੋਜੀ ਦੀ ਵਰਤੋਂ ਲਗਾਤਾਰ ਵਧ ਰਹੀ ਹੈ। {extra}"
]
PUNJABI_EXTRAS = ["ਪੰਜਾਬੀ ਵਿੱਚ ਜਾਣਕਾਰੀ ਪ੍ਰਾਪਤ ਕਰਨਾ ਆਸਾਨ ਹੈ।"]


def generate_corpus(num_documents: int = 5000) -> list:
    """
    Generates num_documents (5,000+) realistic multilingual documents.
    Distribution: ~60% Telugu, 10% Hindi, 5% Tamil, 5% Kannada, 5% Malayalam, 5% Bengali, 5% Marathi, 5% Punjabi.
    """
    documents = []

    print(f"Generating {num_documents} Indian-language Wikipedia style documents...")

    for doc_id in range(1, num_documents + 1):
        topic = random.choice(TOPICS)
        lang_roll = random.random()

        if lang_roll < 0.60:
            lang = "te"
            template = random.choice(TELUGU_TEMPLATES)
            extra = random.choice(TELUGU_EXTRAS)
            title = f"{topic} - వికీపీడియా"
            body = template.format(topic=topic, extra=extra)
            # Add secondary paragraph for realism
            body += " " + random.choice(TELUGU_TEMPLATES).format(topic=random.choice(TOPICS), extra=random.choice(TELUGU_EXTRAS))
        elif lang_roll < 0.70:
            lang = "hi"
            template = random.choice(HINDI_TEMPLATES)
            extra = random.choice(HINDI_EXTRAS)
            title = f"{topic} - विकिपीडिया"
            body = template.format(topic=topic, extra=extra)
        elif lang_roll < 0.75:
            lang = "ta"
            template = random.choice(TAMIL_TEMPLATES)
            extra = random.choice(TAMIL_EXTRAS)
            title = f"{topic} - விக்கிப்பீடியா"
            body = template.format(topic=topic, extra=extra)
        elif lang_roll < 0.80:
            lang = "kn"
            template = random.choice(KANNADA_TEMPLATES)
            extra = random.choice(KANNADA_EXTRAS)
            title = f"{topic} - ವಿಕಿಪೀಡಿಯಾ"
            body = template.format(topic=topic, extra=extra)
        elif lang_roll < 0.85:
            lang = "ml"
            template = random.choice(MALAYALAM_TEMPLATES)
            extra = random.choice(MALAYALAM_EXTRAS)
            title = f"{topic} - വിക്കിപീഡിയ"
            body = template.format(topic=topic, extra=extra)
        elif lang_roll < 0.90:
            lang = "bn"
            template = random.choice(BENGALI_TEMPLATES)
            extra = random.choice(BENGALI_EXTRAS)
            title = f"{topic} - উইকিপিডিয়া"
            body = template.format(topic=topic, extra=extra)
        elif lang_roll < 0.95:
            lang = "mr"
            template = random.choice(MARATHI_TEMPLATES)
            extra = random.choice(MARATHI_EXTRAS)
            title = f"{topic} - विकिपीडिया"
            body = template.format(topic=topic, extra=extra)
        else:
            lang = "pa"
            template = random.choice(PUNJABI_TEMPLATES)
            extra = random.choice(PUNJABI_EXTRAS)
            title = f"{topic} - ਵਿਕੀਪੀਡੀਆ"
            body = template.format(topic=topic, extra=extra)

        doc = {
            "document_id": doc_id,
            "title": title,
            "language": lang,
            "text": body,
            "source": "Wikipedia Sample Dataset"
        }
        documents.append(doc)

    return documents


def main():
    docs = generate_corpus(num_documents=5000)
    RAW_CORPUS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(RAW_CORPUS_PATH, 'w', encoding='utf-8') as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)
    print(f"Successfully generated {len(docs)} documents at: {RAW_CORPUS_PATH}")


if __name__ == "__main__":
    main()

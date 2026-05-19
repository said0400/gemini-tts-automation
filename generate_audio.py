# احتفظ بنفس الدوال (convert_to_wav و parse_audio_mime_type) كما هي في كودك.

def generate():
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-3.1-flash-tts-preview"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""Read the following transcript based on the audio profile and director's note.
# Audio Profile
A vibrant and theatrical host.
# Director's note
Style: Promo/Hype. Pace: Rapid Fire. Accent: Neutral.
## Transcript:
السلام عليكم""")
            ],
        ),
    ]
    
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        response_modalities=["audio"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Zubenelgenubi")
            )
        ),
    )

    print("جاري توليد الصوت من Gemini...")
    all_audio_data = b""
    last_mime_type = "audio/L16;rate=24000"

    # تجميع البث الصوتي
    for chunk in client.models.generate_content_stream(model=model, contents=contents, config=generate_content_config):
        if chunk.parts is None:
            continue
        if chunk.parts[0].inline_data and chunk.parts[0].inline_data.data:
            inline_data = chunk.parts[0].inline_data
            all_audio_data += inline_data.data
            if inline_data.mime_type:
                last_mime_type = inline_data.mime_type
        else:
            if text := chunk.text:
                print(text)

    if all_audio_data:
        # تحويل البيانات المجمعة كاملة إلى صيغة WAV وحفظها
        final_wav_data = convert_to_wav(all_audio_data, last_mime_type)
        save_binary_file("final_output.wav", final_wav_data)
    else:
        print("فشل في توليد الصوت.")

if __name__ == "__main__":
    generate()

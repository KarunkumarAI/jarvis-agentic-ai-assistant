import streamlit as st

from core.controller import handle_request
from voice.speech_to_text import transcribe_audio
from voice.text_to_speech import speak


def handle_prompt(prompt: str) -> None:

    # Save previous conversation BEFORE
    # adding the current question
    history = st.session_state.messages[-10:]

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.write(prompt)

    try:
        with st.spinner("JARVIS is thinking..."):
            response = handle_request(
                prompt,
                history=history,
            )

    except Exception as error:
        response = (
            f"Sorry, something went wrong: {error}"
        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )

    with st.chat_message("assistant"):
        st.write(response)

    if st.session_state.get(
        "voice_enabled",
        False,
    ):
        speak(response)


def show_chat() -> None:

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    audio = st.audio_input(
        "🎤 Speak to JARVIS"
    )

    if audio:
        audio_bytes = audio.getvalue()
        audio_id = hash(audio_bytes)

        if (
            st.session_state.get("last_audio")
            != audio_id
        ):
            st.session_state.last_audio = audio_id

            try:
                prompt = transcribe_audio(
                    audio_bytes
                )

                st.caption(
                    f"You said: {prompt}"
                )

                handle_prompt(prompt)

            except Exception as error:
                st.error(
                    f"Voice recognition failed: {error}"
                )

    prompt = st.chat_input(
        "Ask JARVIS anything..."
    )

    if prompt:
        handle_prompt(prompt)
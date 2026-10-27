
import streamlit as st

from vision.image_analyzer import analyze_image


def show_vision() -> None:
    st.subheader("👁️ JARVIS Vision")

    # ---------------------------------------
    # IMAGE UPLOAD
    # ---------------------------------------
    uploaded_image = st.file_uploader(
        "Upload an image",
        type=["jpg", "jpeg", "png"],
    )

    if uploaded_image is not None:
        st.image(uploaded_image)

        question = st.text_input(
            "Ask something about the image",
            placeholder="What can you see?",
        )

        if st.button("Analyze Image"):
            try:
                with st.spinner("Analyzing image..."):
                    answer = analyze_image(
                        uploaded_image.getvalue(),
                        question or "Describe this image.",
                    )

                st.write(answer)

            except Exception as error:
                st.error(f"Vision failed: {error}")

    st.divider()

    # ---------------------------------------
    # CAMERA CONTROL
    # ---------------------------------------
    if "camera_enabled" not in st.session_state:
        st.session_state.camera_enabled = False

    st.subheader("📷 Camera")

    if not st.session_state.camera_enabled:
        st.info("Camera is OFF.")

        if st.button("📷 Open Camera", key="open_jarvis_camera"):
            st.session_state.camera_enabled = True
            st.rerun()

    else:
        if st.button("⏹ Close Camera", key="close_jarvis_camera"):
            st.session_state.camera_enabled = False
            st.rerun()

        camera_image = st.camera_input(
            "Take a photo",
            key="jarvis_camera_input",
        )

        if camera_image is not None:
            if st.button("Analyze Camera Image"):
                try:
                    with st.spinner("Analyzing camera image..."):
                        answer = analyze_image(
                            camera_image.getvalue(),
                            "Describe what you can see.",
                        )

                    st.write(answer)

                except Exception as error:
                    st.error(f"Camera analysis failed: {error}")

import streamlit as st
from video import video1
from Assitant import assist
from Audio import record_and_save_audio
from suggest import suggest
import numpy as np
import scipy.io.wavfile as waves
from scipy import signal, stats
import plotly.graph_objects as go
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet

# Global variable for transcript
transcript = ""
video_analysis_result = ""
audio_analysis_result = ""
eeg_analysis_result = ""
def smooth_triangle(data, degree):
    triangle = np.concatenate((np.arange(degree + 1), np.arange(degree)[::-1]))  # up then down
    smoothed = []

    for i in range(degree, len(data) - degree * 2):
        point = data[i:i + len(triangle)] * triangle
        smoothed.append(np.sum(point) / np.sum(triangle))
    
    # Handle boundaries
    smoothed = [smoothed[0]] * int(degree + degree/2) + smoothed
    while len(smoothed) < len(data):
        smoothed.append(smoothed[-1])
    
    return smoothed

def generate_pdf():
    doc = SimpleDocTemplate("analysis_report.pdf", pagesize=letter)

    # Content of the PDF
    elements = []

    # Add Video Analysis Result
    elements.append(Paragraph("### Video Analysis Result"))
    elements.append(Image("mood_graph.png", width=400, height=300))
    elements.append(Paragraph("### Audio Analysis Result"))
    elements.append(Paragraph(f"<b>Transcript:</b> {transcript}", style=getSampleStyleSheet()['BodyText']))
    # Add EEG Analysis Result
    elements.append(Paragraph("### EEG Analysis Result"))
    elements.append(Image("spectrogram.png", width=400, height=300))
    elements.append(Image("alpha_power.png", width=400, height=300))
    elements.append(Image("box_plot.png", width=400, height=300))
    # Add EEG analysis plots and results here
    # Build the PDF
    doc.build(elements)

# Rest of your Streamlit code...
def main():
    global transcript, video_analysis_result, audio_analysis_result, eeg_analysis_result

    st.set_page_config(layout="wide")
    st.title("Mind AI 🧠")
    st.subheader("Slogan goes here")
    st.markdown("""
                        -Put on your EEG \n
                        -Let your emotions speak \n
                    """)
    st.subheader("Uploading EEG file")
    st.subheader("Begin the analysis process")

    st.header("Brain Wave Analysis")
    st.caption('Enhance your understanding of mental wellness through EEG data analysis.')

    uploaded_file = st.file_uploader("Upload a WAV File", type=["wav"])
    
    if uploaded_file is not None:
        fs, data = waves.read(uploaded_file)

        length_data = np.shape(data)
        length_new = length_data[0] * 0.05
        ld_int = int(length_new)

        data_new = signal.resample(data, ld_int)

        # Spectrogram
        fig = go.Figure()

        f, t, Sxx = signal.spectrogram(data_new, fs=500, nperseg=256, noverlap=250)
        fig.add_heatmap(x=t, y=f, z=10 * np.log10(Sxx), colorscale='Viridis')

        # Save the spectrogram as an image
        fig.write_image("spectrogram.png")

        st.markdown("### Spectrogram Explanation:")
        st.write("The spectrogram provides a visual representation of the power spectral density over time and frequency.")
        st.write("It helps visualize how different frequencies contribute to the signal, useful for identifying patterns.")

        # Alpha Power Over Time
        position_vector = np.where((f >= 8) & (f <= 13))[0]

        AlphaRange = np.mean(Sxx[position_vector[0]:position_vector[-1] + 1, :], axis=0)

        fig_alpha = go.Figure()
        fig_alpha.add_trace(go.Scatter(x=t, y=smooth_triangle(AlphaRange, 100), mode='lines', name='Alpha Power'))

        # Save the alpha power plot as an image
        fig_alpha.write_image("alpha_power.png")

        # st.markdown("### Alpha Power Over Time Explanation:")
        # st.write("This plot shows the variation in alpha power (8-10 Hz) over time after smoothing.")
        # st.write("Alpha waves are commonly associated with relaxed states.")

        # Statistical Analysis
        tg = np.array([4.2552, 14.9426, 23.2801, 36.0951, 45.4738, 59.3751, 72.0337, 85.0831, max(t) + 1])
        eyesclosed = []
        eyesopen = []
        j = 0  # Initial variable to traverse tg
        l = 0  # Initial variable to loop through the "y" data
        for i in range(0, len(t)):
            if t[i] >= tg[j]:
                if j % 2 == 0:
                    eyesopen.append(np.mean(AlphaRange[l:i]))
                if j % 2 == 1:
                    eyesclosed.append(np.mean(AlphaRange[l:i]))
                l = i
                j = j + 1

        fig_stat = go.Figure()
        fig_stat.add_box(y=eyesopen, name='Eyes Open', boxpoints='all', jitter=0.3, pointpos=-1.8)
        fig_stat.add_box(y=eyesclosed, name='Eyes Closed', boxpoints='all', jitter=0.3, pointpos=-0.6)

        # Save the box plot as an image
        fig_stat.write_image("box_plot.png")

        # st.markdown("### Statistical Analysis Explanation:")
        # st.write("The box plot visually compares the distribution of alpha power during eyes open and eyes closed states.")
        # st.write("The t-test result indicates statistical significance in the difference.")

        # st.write("Mean (Eyes Open):", np.mean(eyesopen))
        # st.write("Mean (Eyes Closed):", np.mean(eyesclosed))
        # st.write("Standard Deviation (Eyes Open):", np.std(eyesopen))
        # st.write("Standard Deviation (Eyes Closed):", np.std(eyesclosed))

        result = stats.ttest_ind(eyesopen, eyesclosed, equal_var=False)
        st.write("T-Test Result:")
        # st.write("t-Statistic:", result.statistic)
        # st.write("p-Value:", result.pvalue)

        position_vector = np.where((f >= 13) & (f <= 20))[0]

        AlphaRange = np.mean(Sxx[position_vector[0]:position_vector[-1] + 1, :], axis=0)

        fig_alpha = go.Figure()
        fig_alpha.add_trace(go.Scatter(x=t, y=smooth_triangle(AlphaRange, 100), mode='lines', name='Alpha Power'))

        # Save the beta power plot as an image
        fig_alpha.write_image("beta_power_lower.png")

        position_vector = np.where((f >= 13) & (f <= 30))[0]

        AlphaRange = np.mean(Sxx[position_vector[0]:position_vector[-1] + 1, :], axis=0)

        fig_alpha = go.Figure()
        fig_alpha.add_trace(go.Scatter(x=t, y=smooth_triangle(AlphaRange, 100), mode='lines', name='Alpha Power'))

        # Save the beta power plot as an image
        fig_alpha.write_image("beta_power_higher.png")

        st.subheader("Record your video")

    if st.button("Click to start recording video!"):
        video1()
        video_analysis_result = "Your video analysis result"

    st.subheader("Record Audio")
    if st.button("Click to start recording audio!"):
        st.write("Transcript: ")
        transcript = record_and_save_audio()
        st.write(transcript)
        audio_analysis_result = transcript

    if st.button("Begin"):
        eeg_analysis_result = "Your EEG analysis result"
        
        # Generate PDF
        generate_pdf()

        analysis = assist(str(result))
        st.write(analysis)
        st.write(suggest(analysis))

if __name__ == "__main__":
    main()

# 📊 Look At Your Data

This web app helps in analyzing datasets in `csv, xlsx, json` formats.
You can upload your files and see some statistics and use provided charts to plot and save the graphs for the data.

---

**Used packages and libraries**
* NumPy
* Pandas
* Plotly
* Streamlit

### How to run and use

1. At first, create new *Python environment* for the app:
	* `mkdir app` - create new directory
	* `cd app` - move to the created directory
	* `python3 -m venv venv` - create new environment
	* `source venv/bin/activate`  - activate env (use `deactivate` to deactivate the env)
2. After, install the dependencies for the app:  `pip3 install -r requirements.txt`
3. Run the app: `streamlit run 1_📊_Statistics.py`

The app will run on your browser at `http://localhost:8501`
<br>
<img width="1440" alt="Screenshot 2023-10-12 at 14 53 48" src="https://github.com/malkhasyann/data_analysis_tool/assets/99897064/611f968e-02fb-4daf-9e6b-5ff3aceccd52">
<br>
It is the **statistics tab** where you can drag and drop your files and choose the file you want to work with.
<br>
<img width="1440" alt="Screenshot 2023-10-12 at 14 57 40" src="https://github.com/malkhasyann/data_analysis_tool/assets/99897064/27b7a7bb-8485-45b7-bb63-0bde3db5bd69">
<br>
The dataset will be shown and some general statistics for dataset columns.<br>
Move to the **visualize tab** to use charts for plotting.
<br>
<img width="1440" alt="Screenshot 2023-10-12 at 15 00 30" src="https://github.com/malkhasyann/data_analysis_tool/assets/99897064/7c614d99-528f-46a0-a1fb-6f1633509873">
<br>
<img width="1440" alt="Screenshot 2023-10-12 at 15 06 16" src="https://github.com/malkhasyann/data_analysis_tool/assets/99897064/0613a754-f1b9-4a6f-a7a7-526a7fdbe2d3">

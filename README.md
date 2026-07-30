create venv to run this project

1.  pip install -r requirements.txt
2. python -m venv venv
3.source venv/bin/activate
python main.py
streamlit run dashboard.py --server.address=0.0.0.0 --server.port=8501 --server.enableCORS=false --server.enableXsrfProtection=false

create venv to run this project

 python -m venv venv
1.  python -m venv venv
2. pip install -r requirements.txt
3.source venv/bin/activate
python main.py
streamlit run dashboard.py --server.address=0.0.0.0 --server.port=8501 --server.enableCORS=false --server.enableXsrfProtection=false

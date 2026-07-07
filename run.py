from app import create_app

try:
    app = create_app()
    
    
except Exception as e:
    print("\nERROR DURING APP CREATION:")
    print(type(e).__name__)
    print(e)
    raise

if __name__ == "__main__":
    app.run(debug=True)
'''
nboudjem python.file
Pour faire des recherches avec un mot clé dans un fichier Excel (inventraire) labo de chimie physiaue!
Lycee Paul Bert
'''
import pandas as pd
from tkinter import Tk, filedialog

def results_fetch(sheets, search_text):
    results = {}  # Store filtered results per sheet

    for sheet_name, df in sheets.items():
        # Set the index to start from 2 (header is treated as row 1)
        df.index = df.index + 2

        # Filter rows where any column contains the search text
        filtered_df = df[
            df.apply(lambda row: row.astype(str).str.contains(search_text, case=False, na=False).any(), axis=1)]

        if not filtered_df.empty:
            results[sheet_name] = filtered_df  # Store results per sheet
    return results

def upload_and_search():
    # Open file dialog to select file
    Tk().withdraw()
    file_path = filedialog.askopenfilename(title="Select File",
                                           filetypes=[("Excel and CSV files", "*.xls;*.xlsx;*.csv")])

    if not file_path:
        print("Aucun fichier sélectionné.")
        return

    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path, dtype=str)  # Read CSV file
            sheets = {"Sheet1": df}  # Treat as a single sheet
        else:
            sheets = pd.read_excel(file_path, sheet_name=None, dtype=str)  # Read all sheets
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier: {e}")
        return

    print("Fichier téléchargé avec succès!")

    # Get search text from user
    search_text = input("Entrez le texte à rechercher: ").strip().lower()
    if not search_text:
        print("Aucun texte de recherche fourni.")
        return

    results = results_fetch(sheets, search_text)

    # Display results
    N = 100
    for i in range(N):
        if not results:
            print("Aucun enregistrement correspondant n'a été trouvé!")
            # Get search text from user
            search_text = input("Entrez le texte à rechercher a nouveau: ").strip().lower()
            if not search_text:
                print("Aucun texte de recherche fourni a nouveau.")
                return
            results = results_fetch(sheets, search_text)
        else:
            pass

    for sheet_name, filtered_df in results.items():
        print(f"\n Résultats trouvés dans la feuille: **{sheet_name}**")
        pd.set_option('display.max_columns', None)
        print(filtered_df.to_string())
        print('----------------------------------------------------------')



    return results


# Run the function
if __name__ == "__main__":
    upload_and_search()

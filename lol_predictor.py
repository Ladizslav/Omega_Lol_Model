import warnings
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings("ignore") 

import pandas as pd
from logical_regression import train_model_lr, evaluate_model_lr, save_model_lr, load_model_lr,predict_win_lr
from neural_network import train_model_nn, evaluate_model_nn, save_model_nn, load_model_nn,predict_win_nn
from random_forest import train_model_rf, evaluate_model_rf, save_model_rf, load_model_rf,predict_win_rf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


class LolPredictor:
    
    # Inicializace objektu
    def __init__(self):
        self.data = None
        self.scaler = None
        self.champion_mapping = None
        self.models = {'lr': None,'rf': None,'nn': None}
        self.input_features = ['duration', 'champion_id', 'gold_per_min', 'damage_per_min', 'kda_ratio']
        
    # Načtení dat ze souborů
    def load_data(self):
        try:
            self.data = pd.read_csv("csv/data.csv")
            self.champion_mapping = pd.read_csv("csv/champion_mapping.csv")
            return True
        except Exception as e:
            print(f"Chyba při načítání dat: {str(e)}")
            return False
    
    # Připrava dat pro trénování
    def prepare_data(self):
        try:
            X_train, X_test, y_train, y_test = train_test_split(self.data[self.input_features], self.data['win'], test_size=0.1)
            self.scaler = StandardScaler()
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            return {'X_train': X_train,'X_test': X_test,'y_train': y_train,'y_test': y_test,'X_train_scaled': X_train_scaled,'X_test_scaled': X_test_scaled}
        except Exception as e:
            print(f"Chyba při přípravě dat: {str(e)}")
            return None
    
    # Natrénování všech modelů
    def train_all_models(self):
        if self.data is None:
            print("Nejdříve načtěte data!")
            return
        prepared_data = self.prepare_data()
        if prepared_data is None:
            return
        self.models['lr'] = train_model_lr(prepared_data['X_train'], prepared_data['y_train'])
        self.models['rf'] = train_model_rf(prepared_data['X_train'], prepared_data['y_train'])
        self.models['nn'] = train_model_nn(prepared_data['X_train_scaled'], prepared_data['y_train'],prepared_data['X_test_scaled'], prepared_data['y_test'])
        print("Všechny modely natrénovány")
    
    # Vyhodnocení všech modelů
    def evaluate_all_models(self):
        try:
            if self.data is None or (prepared_data := self.prepare_data()) is None:
                return print("Nejdříve načtěte a připravte data.")

            print("\nVýsledky vyhodnocení:")
            
            if self.models.get('lr') is not None:
                evaluate_model_lr(self.models['lr'], prepared_data['X_test'], prepared_data['y_test'])
            if self.models.get('rf') is not None:
                evaluate_model_rf(self.models['rf'], prepared_data['X_test'], prepared_data['y_test'])
            if self.models.get('nn') is not None and self.scaler is not None:
                evaluate_model_nn(self.models['nn'], prepared_data['X_test_scaled'], prepared_data['y_test'])
                
        except Exception as e:
            print(f"\nChyba při evaluaci: {str(e)}")
    
    # Uložení všechn modelů
    def save_all_models(self):
        try:
            if self.models['lr'] is not None:
                save_model_lr(self.models['lr'])
                print("Lr model uložen.")
            else:
                print("Lr model není natrénován.")
            if self.models['rf'] is not None:
                save_model_rf(self.models['rf'])
                print("Rf model uložen.")
            else:
                print("Rf model není natrénován.")
            if self.models['nn'] is not None and self.scaler is not None:
                save_model_nn(self.models['nn'], self.scaler)
                print("Nn model uložen.")
            else:
                print("Nn model není natrénován.")

        except Exception as e:
            return print(f"Chyba při ukládání modelů: {str(e)}")

    # Načtení všech modelů
    def load_all_models(self):
        try:
            self.models['lr'] = load_model_lr()
            self.models['rf'] = load_model_rf()
            self.models['nn'], self.scaler = load_model_nn()
            print(f"Načtení všech modelů bylo úspěšné.")
        except Exception as e:
            print(f"Chyba při načítání modelů: {str(e)}")

    # Predikce šanci na výhru
    def predict_win(self):
        if None in self.models.values() or self.champion_mapping is None or self.champion_mapping.empty:
            return print("Nejdříve načtěte data a natrénujte modely.")

        try:
            champ_name = input("\nZadejte jméno championa: ").strip().lower()
            champ = self.champion_mapping[
                self.champion_mapping['champion_name'].str.lower() == champ_name
            ]
            if champ.empty:
                return print("Champion nenalezen!")

            champ_id = champ['champion_id'].values[0]
            print(f"Vybraný: {champ['champion_name'].values[0]}")

            inputs = {
                'duration': int(input("Minuty hry: ")) * 60 + int(input("Sekundy hry: ")),
                'gold': float(input("Celkové zlato: ")),
                'damage': float(input("Celkové poškození: ")),
                'kills': float(input("Zabití: ")),
                'deaths': float(input("Úmrtí: ")),
                'assists': float(input("Asistence: "))
            }

            stats = [
                inputs['duration'],
                champ_id,
                inputs['gold'] / (inputs['duration'] / 60),
                inputs['damage'] / (inputs['duration'] / 60),
                (inputs['kills'] + inputs['assists']) / max(inputs['deaths'], 1)
            ]

            stats_df = pd.DataFrame([stats], columns=self.input_features)

            print("\nŠance na výhru:")

            prob_lr = predict_win_lr(self.models['lr'], stats_df) * 100
            if prob_lr is not None:
                print(f"LR: {prob_lr}%")

            prob_rf = predict_win_rf(self.models['rf'], stats_df) * 100
            if prob_rf is not None:
                print(f"RF: {prob_rf}%")

            prob_nn = predict_win_nn(self.models['nn'], self.scaler, stats_df.values) * 100
            if prob_nn is not None:
                print(f"NN: {prob_nn}% ")

        except Exception as e:
            print(f"\nChyba při predikování: {str(e)}")

    # Zobrazí hlavní menu
    def show_menu(self):
        print("\n------ Main menu ------")
        print("1. Načíst data")
        print("2. Trénovat modely")
        print("3. Vyhodnotit modely")
        print("4. Uložit modely")
        print("5. Načíst modely")
        print("6. Predikovat výhru")
        print("0. Konec")
        
        try:
            choice = int(input("\nVyberte akci: "))
            return choice
        except:
            return -1
    
    # Hlavní smyčka aplikace
    def run(self):
        while True:
            choice = self.show_menu()
            
            if choice == 0:
                print("Ukončuji program...")
                break
                
            elif choice == 1:
                if self.load_data():
                    print("Data úspěšně načtena!")
                
            elif choice == 2:
                self.train_all_models()
                
            elif choice == 3:
                self.evaluate_all_models()
                
            elif choice == 4:
                self.save_all_models()
                
            elif choice == 5:
                self.load_all_models()
                
            elif choice == 6:
                self.predict_win()
                
            else:
                print("Neplatná volba, zkuste to znovu.")

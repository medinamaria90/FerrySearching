from abc import ABC, abstractmethod
from datetime import datetime
import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

load_dotenv()

# Base Class.
class BaseSupplier(ABC):
    conversion = {
        "ALGE": "Algeciras",
        "CEUT": "Ceuta",
        "TANM": "Tanger Med",
        "FAST_FERRY": "Fast Ferry",
    }
    option_counter = 1
    def __init__(self, form):
        form.is_valid()
        self.date = form.cleaned_data['depart_date']
        self.route = form.cleaned_data['route']
        self.departurePort = form.cleaned_data['route'][:4]
        self.arrivalPort = form.cleaned_data['route'][-4:]
        self.return_date = form.cleaned_data['return_date']

    # This method has to be implemented by the subclass
    @abstractmethod
    def get_data(self):
        pass

	# This method has to be implemented by the subclass
    @abstractmethod
    def normalize_data(self, data):
        pass

    def split_datetime(self, datetime_str, format='%Y-%m-%d %H:%M %p'):
        dt = datetime.strptime(datetime_str, format)
        return {
            "date": dt.strftime('%d/%m/%Y'),
            "time": dt.strftime('%H:%M')
        }

# Supplier 1 API Class.
class Supplier1(BaseSupplier):
    SUPPLIER_1_ENDPOINT = "https://tadpole-1.clickferry.app/timetable"
    SUPPLIER_1_TOKEN = os.getenv('SUPPLIER_1_TOKEN')

    def get_data(self, is_departure):
        if is_departure == True:
            date = self.date
            departurePort = self.departurePort
            arrivalPort = self.arrivalPort
        else:
            date = self.return_date
            departurePort = self.arrivalPort
            arrivalPort = self.departurePort
        headers = {"Authorization": f"Bearer {self.SUPPLIER_1_TOKEN}"}
        params = {
            "date": date,
            "departurePort": departurePort,
            "arrivalPort": arrivalPort,
        }
        response = requests.get(
            url=self.SUPPLIER_1_ENDPOINT, headers=headers, params=params)
        return response.json()

    def normalize_data(self, data, is_departure):
        normalized_data = []
        if is_departure == True:
            date = self.date
        else:
            date = self.return_date
        for ferri in data:
            if ferri["ship"]["tipo"] == 'FAST_FERRY':
                ferri_type = 'Fast Ferri'
            else:
                ferri_type = ferri["ship"]["tipo"]
            if is_departure == True:
                departurePort = self.departurePort
                arrivalPort = self.arrivalPort
            else:
                departurePort = self.arrivalPort
                arrivalPort = self.departurePort
            departure_datetime = self.split_datetime(ferri["departure"])
            arrival_datetime = self.split_datetime(ferri["arrival"])
            normalized_data.append({
                "option": BaseSupplier.option_counter,
                "supplier": "1",
                "from": self.conversion.get(departurePort),
                "to": self.conversion.get(arrivalPort),
                "date": departure_datetime["date"],
                "time": departure_datetime["time"],
                "arrivalDate": arrival_datetime["date"],
                "arrivalTime": arrival_datetime["time"],
                "ship": ferri["ship"]["name"],
                "ship_type": ferri_type,
            })
        BaseSupplier.option_counter += 1
        return normalized_data

# Supplier 2 API Class.
class Supplier2(BaseSupplier):
    SUPPLIER_2_LOGIN_ENDPOINT = "https://tadpole-2.clickferry.app/login"
    SUPPLIER_2_TIMETABLE_ENDPOINT = "https://tadpole-2.clickferry.app/timetable/"
    SUPPLIER_2_USERNAME = os.getenv('SUPPLIER_2_USERNAME')
    SUPPLIER_2_PASSWORD = os.getenv('SUPPLIER_2_PASSWORD')

    def get_data(self, is_departure):
        if is_departure == True:
            date = self.date
            route = self.route
        else:
            date = self.return_date
            route = self.route[4:] + self.route[:4]
        token = self.get_bearer_auth()
        headers = {"Authorization": f"Bearer {token}"}
        params = {"start": date, "end": date}
        response = requests.get(
            url=f"{self.SUPPLIER_2_TIMETABLE_ENDPOINT}{route}", headers=headers, params=params)
        return response.json()

    def get_bearer_auth(self):
        response = requests.post(self.SUPPLIER_2_LOGIN_ENDPOINT, auth=HTTPBasicAuth(
            self.SUPPLIER_2_USERNAME, self.SUPPLIER_2_PASSWORD))
        token = response.json().get("token")
        return token

    def normalize_data(self, data, is_departure):
        normalized_data = []
        if is_departure == True:
            date = self.date
            departurePort = self.departurePort
            arrivalPort = self.arrivalPort
        else:
            date = self.return_date
            departurePort = self.arrivalPort
            arrivalPort = self.departurePort
        ferries = data["departures"][f"{date}"]

        for ferri in ferries:
            departure_datetime = self.split_datetime(
                str(self.date), format='%Y-%m-%d')['date']
            arrival_datetime = self.split_datetime(
                ferri["arrival"], format='%Y-%m-%dT%H:%M:%S')
            normalized_data.append({
                "option": BaseSupplier.option_counter,
                "supplier": "2",
                "from": self.conversion.get(departurePort),
                "to": self.conversion.get(arrivalPort),
                "date": departure_datetime,
                "time": ferri["time"][:5],
                "arrivalDate": arrival_datetime["date"],
                "arrivalTime": arrival_datetime["time"],
                "ship": ferri["ship"]["name"].title(),
                "ship_type": ferri["ship"]["type"],
            })
        BaseSupplier.option_counter += 1
        return normalized_data

# Supplier Manager. Introduce the new suppliers classes in the self.suppliers list
class SupplierManager:
    def __init__(self, form):
        self.suppliers = [Supplier1(form), Supplier2(form)]
        self.date = form.cleaned_data['depart_date']
        self.return_date = form.cleaned_data['return_date']

    def get_all_suppliers(self):
        BaseSupplier.option_counter = 1
        departures = []
        for supplier in self.suppliers:
            data = supplier.get_data(is_departure=True)
            normalized_data = supplier.normalize_data(data, is_departure=True)
            departures.extend(normalized_data)
        if (self.return_date != None):
            returns = []
            for supplier in self.suppliers:
                data = supplier.get_data(is_departure=False)
                normalized_data = supplier.normalize_data(
                    data, is_departure=False)
                returns.extend(normalized_data)
        else:
            returns = None
        results = {
            'departures': departures,
            'returns': returns,
        }
        return results

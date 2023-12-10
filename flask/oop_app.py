from flask import Flask, render_template, request
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pymysql
import paramiko
from ssh_conn import execute_command_on_vm

class DatabaseConnector:
    def connect(self):
        # Your connect function here...

class DataFetcher:
    def __init__(self, database_connector):
        self.database_connector = database_connector

    def get_statistic(self, location=None):
        # Your get_statistic function here...

    def get_raw_data(self, amount, location=None):
        # Your get_raw_data function here...

class ChartMaker:
    def generate_pie_chart(self, data_dict):
        # Your generate_pie_chart function here...

    def generate_bar_chart(self, data_dict):
        # Your generate_bar_chart function here...

class Routes:
    def __init__(self, app, data_fetcher, chart_maker):
        self.app = app
        self.data_fetcher = data_fetcher
        self.chart_maker = chart_maker

        self.setup_routes()

    def base(self):
        return render_template('base.html')

    def total(self):
        # Your total function here...

    def per_region(self):
        # Your per_region function here...

    def raw_data(self):
        # Your raw_data function here...

    def check_credentials(self, username, password):
        return username == 'admin' and password == 'test'

    def admin(self):
        # Your admin function here...

    def toggle_device(self):
        # Your toggle_device function here...

    def setup_routes(self):
        self.app.route('/')(self.base)
        self.app.route('/total')(self.total)
        self.app.route('/per_region')(self.per_region)
        self.app.route('/raw_data', methods=['GET', 'POST'])(self.raw_data)
        self.app.route('/admin', methods=['GET', 'POST'])(self.admin)
        self.app.route('/admin/toggle', methods=['POST'])(self.toggle_device)

if __name__ == '__main__':
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'auhue'

    database_connector = DatabaseConnector()
    data_fetcher = DataFetcher(database_connector)
    chart_maker = ChartMaker()

    routes = Routes(app, data_fetcher, chart_maker)
    app.run(debug=True)
 # Ensure to import paramiko

class SSHClientMaker:
    @staticmethod
    def create_ssh_client():
        host = '192.168.1.12'
        port = 22
        user = 'test'
        password = 'test'

        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(host, port=port, username=user, password=password)
        return client

class SSHOperations:
    @staticmethod
    def find_pid_by_name(process_name, ssh_client):
        command = f"pgrep -f {process_name}"
        stdin, stdout, stderr = ssh_client.exec_command(command)
        pid = stdout.read().decode().strip().split()
        return pid

    @staticmethod
    def check_database_status(ssh_client):
        command = 'ps aux | grep mysql'
        stdin, stdout, stderr = ssh_client.exec_command(command)
        process_list = stdout.read().decode()
        if 'mysqld' in process_list:
            return 'On'
        else:
            return 'Off'

    @staticmethod
    def check_mqtt_sub_status(ssh_client):
        command = 'ps aux | grep mqtt_sub.py'
        stdin, stdout, stderr = ssh_client.exec_command(command)
        process_list = stdout.read().decode()
        if 'python3 mqtt_sub.py' in process_list:
            return "On"
        else:
            return "Off"

    @staticmethod
    def mqtt_broker_status(ssh_client):
        command = 'ps aux | grep Mqtt_custom_broker'
        stdin, stdout, stderr = ssh_client.exec_command(command)
        process_list = stdout.read().decode()

        if 'Mqtt_custom_broker' in process_list:
            return 'On'
        else:
            return 'Off'

    @staticmethod
    def start_mqtt_subscriber(ssh_client):
        try:
            cmd = 'python3 mqtt_sub.py'
            stdin, stdout, stderr = ssh_client.exec_command(cmd)
            print("MQTT subscriber script started.")
        finally:
            ssh_client.close()

    @staticmethod
    def stop_mqtt_subscriber(ssh_client):
        pid_list = SSHOperations.find_pid_by_name('mqtt_sub.py', ssh_client)
        for i in pid_list:
            ssh_client.exec_command(f"kill {i}")

    @staticmethod
    def execute_command_on_vm(cmd):
        client = SSHClientMaker.create_ssh_client()
        if cmd == 'start':
            SSHOperations.start_mqtt_subscriber(client)
        elif cmd == 'stop':
            SSHOperations.stop_mqtt_subscriber(client)
        elif cmd == 'Database':
            return SSHOperations.check_database_status(client)
        elif cmd == 'Mqtt_Sub':
            return SSHOperations.check_mqtt_sub_status(client)
        print('cmd', cmd)

# Rest of your existing code...

if __name__ == '__main__':
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'auhue'

    database_connector = DatabaseConnector()
    data_fetcher = DataFetcher(database_connector)
    chart_maker = ChartMaker()
    ssh_operations = SSHOperations()

    routes = Routes(app, data_fetcher, chart_maker, ssh_operations)
    app.run(debug=True)

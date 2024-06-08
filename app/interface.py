import tkinter as tk
from tkinter import ttk, messagebox
from app.db import get_db
from app.logica import create_reserva, configurar_estacionamento, get_all_reservas
from app.models import Reservas, Estacionamentos
import datetime

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Estacionamentos")
        self.geometry("600x400")

        self.main_frame = tk.Frame(self)
        self.config_frame = tk.Frame(self)
        self.reserva_frame = tk.Frame(self)
        self.list_reserva_frame = tk.Frame(self)
        self.detail_reserva_frame = tk.Frame(self)

        self.label = tk.Label(self.main_frame, text="Sistema de Estacionamentos")
        self.label.pack(pady=10)
        
        self.configurar_estacionamento_button = tk.Button(self.main_frame, text="Configurar Estacionamento", command=self.show_tela_config)
        self.configurar_estacionamento_button.pack(pady=10)

        self.create_reserva_button = tk.Button(self.main_frame, text="Cadastrar Nova Reserva", command=self.show_tela_reserva)
        self.create_reserva_button.pack(pady=10)


        self.list_reserva_button = tk.Button(self.main_frame, text="Carros Estacionados", command=self.show_lista_reserva)
        self.list_reserva_button.pack(pady=10)

        self.main_frame.pack(fill="both", expand=True)
        self.create_tela_config()
        self.create_tela_reserva()
        self.create_tela_lista()
        self.create_tela_detalhes()

    def create_tela_config(self):
        self.label_config = tk.Label(self.config_frame, text="Configurar Estacionamento")
        self.label_config.pack(pady=10)

        self.nome_label = tk.Label(self.config_frame, text="Nome:")
        self.nome_label.pack()
        self.nome_entry = tk.Entry(self.config_frame)
        self.nome_entry.pack()

        self.tarifa_label = tk.Label(self.config_frame, text="Tarifa por Hora:")
        self.tarifa_label.pack()
        self.tarifa_entry = tk.Entry(self.config_frame)
        self.tarifa_entry.pack()

        self.vagas_label = tk.Label(self.config_frame, text="Vagas:")
        self.vagas_label.pack()
        self.vagas_entry = tk.Entry(self.config_frame)
        self.vagas_entry.pack()

        self.submit_button = tk.Button(self.config_frame, text="Cadastrar", command=self.submit_config)
        self.submit_button.pack(pady=10)

        self.back_button = tk.Button(self.config_frame, text="Voltar", command=self.show_main_frame)
        self.back_button.pack(pady=10)

    def create_tela_reserva(self):
        self.label_reserva = tk.Label(self.reserva_frame, text="Adicionar Carro")
        self.label_reserva.pack(pady=10)

        self.placa_cliente_label = tk.Label(self.reserva_frame, text="Placa Cliente:")
        self.placa_cliente_label.pack()
        self.placa_cliente_entry = tk.Entry(self.reserva_frame)
        self.placa_cliente_entry.pack()

        self.telefone_cliente_label = tk.Label(self.reserva_frame, text="Telefone Cliente:")
        self.telefone_cliente_label.pack()
        self.telefone_cliente_entry = tk.Entry(self.reserva_frame)
        self.telefone_cliente_entry.pack()

        self.submit_reserva_button = tk.Button(self.reserva_frame, text="Cadastrar", command=self.submit_reserva)
        self.submit_reserva_button.pack(pady=10)

        self.back_button = tk.Button(self.reserva_frame, text="Voltar", command=self.show_main_frame)
        self.back_button.pack(pady=10)

    def create_tela_lista(self):
        self.label_list_reserva = tk.Label(self.list_reserva_frame, text="Lista de Reservas")
        self.label_list_reserva.pack(pady=10)

        self.reserva_tree = ttk.Treeview(self.list_reserva_frame, columns=("ID", "Placa Cliente", "Telefone Cliente", "Hora Reserva", "Hora Saida"), show="headings")
        self.reserva_tree.heading("ID", text="ID")
        self.reserva_tree.heading("Placa Cliente", text="Placa Cliente")
        self.reserva_tree.heading("Telefone Cliente", text="Telefone Cliente")
        self.reserva_tree.heading("Hora Reserva", text="Hora Reserva")
        self.reserva_tree.heading("Hora Saida", text="Hora Saida")
        self.reserva_tree.pack(fill="both", expand=True)
        
        self.reserva_tree.bind("<Double-1>", self.show_detail_reserva_frame)

        self.back_button = tk.Button(self.list_reserva_frame, text="Voltar", command=self.show_main_frame)
        self.back_button.pack(pady=10)   

    def create_tela_detalhes(self):
        self.label_detail_reserva = tk.Label(self.detail_reserva_frame, text="Detalhes da Reserva")
        self.label_detail_reserva.pack(pady=10)

        self.detail_text = tk.Text(self.detail_reserva_frame, height=10, width=50)
        self.detail_text.pack(pady=10)

        self.end_reserva_button = tk.Button(self.detail_reserva_frame, text="Encerrar Reserva", command=self.end_reserva)
        self.end_reserva_button.pack(pady=10)

        self.back_button = tk.Button(self.detail_reserva_frame, text="Voltar", command=self.show_lista_reserva)
        self.back_button.pack(pady=10)   

    def show_tela_reserva(self):
        self.main_frame.pack_forget()
        self.config_frame.pack_forget()
        self.list_reserva_frame.pack_forget()
        self.detail_reserva_frame.pack_forget()
        vagas_disponiveis = self.get_vagas_disponiveis()
        self.label_reserva['text'] = f"Adicionar Carro - Vagas Disponíveis: {vagas_disponiveis}"
        self.reserva_frame.pack(fill="both", expand=True)

    def show_tela_config(self):
        self.main_frame.pack_forget()
        self.reserva_frame.pack_forget()
        self.list_reserva_frame.pack_forget()
        self.detail_reserva_frame.pack_forget()
        self.config_frame.pack(fill="both", expand=True)

    def show_lista_reserva(self, event=None):
        self.main_frame.pack_forget()
        self.config_frame.pack_forget()
        self.reserva_frame.pack_forget()
        self.detail_reserva_frame.pack_forget()
        self.list_reserva_frame.pack(fill="both", expand=True)
        self.preencher_lista()

    def show_detail_reserva_frame(self, event):
        selected_item = self.reserva_tree.selection()
        if selected_item:
            item = self.reserva_tree.item(selected_item)
            reserva_data = item['values']
            self.detail_text.delete(1.0, tk.END)
            self.detail_text.insert(tk.END, f"ID: {reserva_data[0]}\n")
            self.detail_text.insert(tk.END, f"Placa Cliente: {reserva_data[1]}\n")
            self.detail_text.insert(tk.END, f"Telefone Cliente: {reserva_data[2]}\n")
            self.detail_text.insert(tk.END, f"Hora Reserva: {reserva_data[3]}\n")
            self.detail_text.insert(tk.END, f"Hora Saida: {reserva_data[4]}\n")
            self.detail_reserva_frame.pack(fill="both", expand=True)
            self.list_reserva_frame.pack_forget()
            self.selected_reserva_id = reserva_data[0]
            self.selected_reserva_data = reserva_data

    def show_main_frame(self):
        self.config_frame.pack_forget()
        self.reserva_frame.pack_forget()
        self.list_reserva_frame.pack_forget()
        self.detail_reserva_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)

    def get_vagas_disponiveis(self):
        db = next(get_db())
        estacionamento = db.query(Estacionamentos).filter(Estacionamentos.id == 1).first()  
        return estacionamento.vagas

    def configurar_estacionamento(self, nome, tarifaHora, vagas):
        db = next(get_db())
        configurar_estacionamento(db, id=1, nome=nome, tarifaHora=tarifaHora, vagas=vagas)  
        tk.messagebox.showinfo("Info", "Estacionamento Configurado")

    def submit_config(self):
        nome = self.nome_entry.get()
        tarifaHora = int(self.tarifa_entry.get())
        vagas = int(self.vagas_entry.get())
        self.configurar_estacionamento(nome, tarifaHora, vagas)
        self.show_main_frame()

    def submit_reserva(self):
        placa_cliente = self.placa_cliente_entry.get()
        telefone_cliente = self.telefone_cliente_entry.get()     
        db = next(get_db())
        estacionamento = db.query(Estacionamentos).filter(Estacionamentos.id == 1).first()  
        if estacionamento.vagas > 0:
            create_reserva(db, estacionamento_id=1, placa_cliente=placa_cliente, telefone_cliente=telefone_cliente, hora_reserva=datetime.datetime.now().hour, hora_saida=None)
            estacionamento.vagas -= 1
            db.commit()
            tk.messagebox.showinfo("Info", "Reserva criada")
        else:
            tk.messagebox.showerror("Error", "Sem vagas")
        self.show_main_frame()

    def preencher_lista(self):
        self.reserva_tree.delete(*self.reserva_tree.get_children())
        db = next(get_db())
        reservas = get_all_reservas(db)
        for reserva in reservas:
            self.reserva_tree.insert("", "end", values=(reserva.id, reserva.placa_cliente, reserva.telefone_cliente, reserva.hora_reserva, reserva.hora_saida))

    def end_reserva(self):
        db = next(get_db())
        selected_reserva = db.query(Reservas).filter(Reservas.id == self.selected_reserva_id).first()
        if selected_reserva:
            hora_saida = datetime.datetime.now().hour
            selected_reserva.hora_saida = hora_saida
            db.commit()

            tarifa = db.query(Estacionamentos.tarifaHora).filter(Estacionamentos.id == selected_reserva.estacionamento_id).scalar()
            hours_stayed = hora_saida - selected_reserva.hora_reserva
            amount_due = hours_stayed * tarifa

            estacionamento = db.query(Estacionamentos).filter(Estacionamentos.id == selected_reserva.estacionamento_id).first()
            estacionamento.vagas += 1
            db.commit()

            self.detail_text.insert(tk.END, f"\nTotal a Pagar: {amount_due} R$")
            tk.messagebox.showinfo("Info", f"Reserva Encerrada. Total a Pagar: {amount_due} R$")
            self.show_lista_reserva()

if __name__ == "__main__":
    app = App()
    app.mainloop()

class Observer:
    def __init__(self, name):
        self.name = name

    def modifier(self, message):
        print(f"{self.name} a recu le message {message}")

class Sujet:
    def __init__(self):
        self.observers = []

    def ajouter(self, observer):
        self.observers.append(observer)

    def notifier(self, message):
        for observer in self.observers:
            observer.modifier(message)
        
if __name__ == '__main__':
    observateur1 = Observer("observateur1")
    observateur2 = Observer("observateur2")
    obeservateur3 = Observer("observateur3")

s = Sujet()
s.ajouter(observateur1)
s.ajouter(observateur2)
s.notifier()


s.ajouter(observateur3)
s.notifier()
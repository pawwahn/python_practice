class Employee:

    raise_amt = 1.05
    def __init__(self,first_name, last_name,pay):
        self.first = first_name
        self.last = last_name
        self.pay = pay

    @property
    def email(self):
        return '{}{}@email.com'.format(self.first,self.last)

    @property
    def full_name(self):
        return '{}{}'.format(self.first,self.last)

    def apply_raise(self):
        self.pay = self.pay * self.raise_amt
        return self.pay

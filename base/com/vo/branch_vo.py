from base import db


class BranchVO(db.Model):
    __tablename__ = 'branch_table'
    branch_id = db.Column('branch_id', db.Integer, primary_key=True,
                          autoincrement=True)
    branch_name = db.Column('branch_name', db.String(255), nullable=False)
    branch_address = db.Column('branch_address', db.Text,
                               nullable=False)
    branch_contact = db.Column('branch_contact', db.String(10), nullable=False)
    branch_manager = db.Column('branch_manager', db.String(255),
                               nullable=False)

    def as_dict(self):
        return {
            'branch_id': self.branch_id,
            'branch_name': self.branch_name,
            'branch_address': self.branch_address,
            'branch_contact': self.branch_contact,
            'branch_manager': self.branch_address,
        }


db.create_all()

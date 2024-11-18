from base import db
from base.com.vo.branch_vo import BranchVO


class CameraVO(db.Model):
    __tablename__ = 'camera_table'
    camera_id = db.Column('camera_id', db.Integer, primary_key=True,
                          autoincrement=True)
    camera_name = db.Column('camera_name', db.String(255), nullable=False)
    camera_code = db.Column('camera_code', db.Text, nullable=False)
    camera_image_name = db.Column('camera_image_name', db.String(255),
                                  nullable=False)
    camera_image_path = db.Column('camera_image_path', db.String(255),
                                  nullable=False)
    camera_branch_id = db.Column('camera_branch_id', db.Integer,
                                 db.ForeignKey(BranchVO.branch_id,
                                               ondelete='CASCADE',
                                               onupdate='CASCADE'),
                                 nullable=False)

    def as_dict(self):
        return {
            'camera_id': self.camera_id,
            'camera_name': self.camera_name,
            'camera_code': self.camera_code,
            'camera_image_name': self.camera_image_name,
            'camera_image_path': self.camera_image_path,
            'camera_branch_id': self.camera_branch_id
        }


db.create_all()

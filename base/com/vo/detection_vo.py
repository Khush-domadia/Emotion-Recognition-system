from base import db
from base.com.vo.branch_vo import BranchVO
from base.com.vo.camera_vo import CameraVO


class DetectionVO(db.Model):
    _tablename_ = 'detection_table'
    detection_id = db.Column("detection_id", db.Integer, primary_key=True,
                             autoincrement=True)
    happy_face = db.Column("happy_face", db.Float)
    sad_face = db.Column("sad_face", db.Float)
    angry_face = db.Column("angry_face", db.Float)
    fear_face = db.Column("fear_face", db.Float)
    neutral_face = db.Column("neutral_face", db.Float)
    surprise_face = db.Column("surprise_face", db.Float)
    disgust_face = db.Column("disgust_face", db.Float)

    detection_branch_id = db.Column('detection_branch_id', db.Integer,
                                    db.ForeignKey(BranchVO.branch_id,
                                                  ondelete='CASCADE',
                                                  onupdate='CASCADE'),
                                    nullable=False)
    detection_camera_id = db.Column('detection_camera_id', db.Integer,
                                    db.ForeignKey(
                                        CameraVO.camera_id,
                                        ondelete='CASCADE',
                                        onupdate='CASCADE'), nullable=False)

    def as_dict(self):
        return {
            'detection_id': self.detection_id,
            'happy_face': self.happy_face,
            'sad_face': self.sad_face,
            'angry_face': self.angry_face,
            'neutral_face': self.neutral_face,
            'surprise_face': self.surprise_face,
            'disgust_face': self.disgust_face,
            'detection_branch_id': self.detection_branch_id,
            'detection_camera_id': self.detection_camera_id,
        }


db.create_all()

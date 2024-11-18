from base import db
from base.com.vo.branch_vo import BranchVO
from base.com.vo.camera_vo import CameraVO
from base.com.vo.detection_vo import DetectionVO
class DetectionDAO:
    def insert_detection(self, detection_vo):
        db.session.add(detection_vo)
        db.session.commit()

    def view_detection(self):
        detection_vo_list = db.session.query(BranchVO, CameraVO,
                                             DetectionVO) \
            .filter(BranchVO.branch_id == DetectionVO.detection_branch_id) \
            .filter(
            CameraVO.camera_id == DetectionVO.detection_camera_id) \
            .all()
        return detection_vo_list

    def delete_detection(self, detection_vo):
        detection_vo_list = DetectionVO.query.get(detection_vo.detection_id)
        db.session.delete(detection_vo_list)
        db.session.commit()
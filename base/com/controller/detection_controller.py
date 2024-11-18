from flask import render_template, request, jsonify,redirect
from base import app
from base.com.dao.branch_dao import BranchDAO
from base.com.dao.camera_dao import CameraDAO
from base.com.dao.detection_dao import DetectionDAO
from base.com.vo.camera_vo import CameraVO
from base.com.vo.detection_vo import DetectionVO
from base.services.live_face import show_webcam

global angry_average_id
global happy_average_id
global sad_average_id
global fear_average_id
global disgust_average_id
global neutral_average_id
global surprise_average_id


@app.route("/load_detection")
def detection():
    branch_dao = BranchDAO()
    branch_vo_list = branch_dao.view_branch()
    return render_template('admin/detection.html',
                           branch_vo_list=branch_vo_list)


@app.route('/admin/ajax_detection')
def admin_ajax_detection():
    camera_vo = CameraVO()
    camera_dao = CameraDAO()
    camera_branch_id = request.args.get('detectionBranchId')
    print(">>>>>>>>>>", camera_branch_id)
    camera_vo.camera_branch_id = camera_branch_id
    camera_vo_list = camera_dao.view_ajax_camera_detection(
        camera_vo)
    ajax_detection_camera = [i.as_dict() for i in camera_vo_list]
    return jsonify(ajax_detection_camera)


@app.route('/admin/insert_detection', methods=['POST'])
def admin_insert_detection():
    detection_branch_id = request.form.get('detectionBranchId')
    detection_camera_id = request.form.get('detectionCameraId')
    print("detection_camera_id>>>>>>>",detection_camera_id)
    # angry_average_id =0.0
    # happy_average_id=0.0
    # sad_average_id=0.0
    # fear_average_id=0.0
    # disgust_average_id=0.0
    # neutral_average_id=0.0
    # surprise_average_id=0.0

    web_cam = show_webcam()
    # emotion= calculate_emotion_averages(angry_average_id, happy_average_id,
    #                                     sad_average_id,disgust_average_id,
    #                                     neutral_average_id,
    #                                     surprise_average_id,fear_average_id)
    print("Controller <>>>>>>>>>>>>>>>>>>>>",web_cam)
    print("Angry--->",web_cam['angry'])
    detection_vo = DetectionVO()
    detection_dao = DetectionDAO()

    detection_vo.detection_branch_id = detection_branch_id
    detection_vo.detection_camera_id = detection_camera_id
    detection_vo.angry_face=web_cam['angry']
    detection_vo.sad_face=web_cam['sad']
    detection_vo.happy_face=web_cam['happy']
    detection_vo.disgust_face=web_cam['disgust']
    detection_vo.surprise_face=web_cam['surprise']
    detection_vo.neutral_face=web_cam['neutral']
    detection_vo.fear_face=web_cam['fear']
    detection_dao.insert_detection(detection_vo)
    # return render_template('admin/addDetection.html')
    return redirect("/admin/view_detection")

@app.route('/admin/view_detection')
def admin_view_detection():
    detection_dao = DetectionDAO()
    detection_vo_list = detection_dao.view_detection()
    print("----->",detection_vo_list)
    return render_template('admin/viewDetection.html',
                           detection_vo_list=detection_vo_list)

@app.route('/admin/delete_detection')
def admin_delete_detection():
    detection_vo = DetectionVO()
    detection_dao = DetectionDAO()
    detection_id = request.args.get('detectionId')
    print(">>>>>>>>", detection_id)
    detection_vo.detection_id = detection_id
    detection_dao.delete_detection(detection_vo)
    return redirect("/admin/view_detection")
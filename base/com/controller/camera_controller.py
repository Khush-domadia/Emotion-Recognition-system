import os

from flask import render_template, request, redirect
from werkzeug.utils import secure_filename

from base import app
from base.com.dao.branch_dao import BranchDAO
from base.com.dao.camera_dao import CameraDAO
from base.com.vo.camera_vo import CameraVO

CAMERA_FOLDER = 'base/static/adminResources/camera/'
app.config['CAMERA_FOLDER'] = CAMERA_FOLDER


@app.route("/loadcamera")
def camera():
    branch_dao = BranchDAO()
    branch_vo_list = branch_dao.view_branch()
    return render_template("admin/addCamera.html",
                           branch_vo_list=branch_vo_list)


@app.route('/admin/insert_camera', methods=['POST'])
def admin_insert_camera():
    camera_name = request.form.get('cameraName')
    camera_code = request.form.get('cameraCode')
    camera_image = request.files.get('cameraImage')
    camera_branch_id = request.form.get('cameraBranchId')
    print(">>>>>>>>>", camera_branch_id)
    camera_image_name = secure_filename(camera_image.filename)
    camera_image_path = os.path.join(app.config['CAMERA_FOLDER'])
    camera_image.save(
        os.path.join(camera_image_path, camera_image_name))

    camera_vo = CameraVO()
    camera_dao = CameraDAO()

    camera_vo.camera_name = camera_name
    camera_vo.camera_code = camera_code
    camera_vo.camera_branch_id = camera_branch_id
    camera_vo.camera_image_name = camera_image_name
    camera_vo.camera_image_path = camera_image_path.replace("base",
                                                            "..")

    camera_dao.insert_camera(camera_vo)
    return redirect('/admin/view_camera')
    # return render_template("admin/home.html")


@app.route('/admin/view_camera')
def admin_view_camera():
    camera_dao = CameraDAO()
    camera_vo_list = camera_dao.view_camera()
    print('camera_vo_list?????', camera_vo_list)
    return render_template('admin/viewCamera.html',
                           camera_vo_list=camera_vo_list)


@app.route('/admin/delete_camera')
def admin_delete_camera():
    camera_vo = CameraVO()
    camera_dao = CameraDAO()
    camera_id = request.args.get('cameraId')
    print(">>>>>>>>", camera_id)
    camera_vo.camera_id = camera_id
    camera_dao.delete_camera(camera_vo)
    # camera_vo_list = camera_dao.delete_camera(camera_id)
    # file_path = camera_vo_list.camera_image_path.replace("..",
    #                                "base") + camera_dao.camera_image_name
    # os.remove(file_path)
    return redirect('/admin/view_camera')


#
@app.route('/admin/edit_camera', methods=['GET'])
def admin_edit_camera():
    camera_vo = CameraVO()
    camera_dao = CameraDAO()
    branch_dao = BranchDAO()

    camera_id = request.args.get('cameraId')
    print(">>>>>", camera_id)
    camera_vo.camera_id = camera_id
    camera_vo_list = camera_dao.edit_camera(camera_vo)
    branch_vo_list = branch_dao.view_branch()
    return render_template('admin/editCamera.html',
                           camera_vo_list=camera_vo_list,
                           branch_vo_list=branch_vo_list)


@app.route('/admin/update_camera', methods=['POST'])
def admin_update_camera():
    camera_id = request.form.get('cameraId')
    camera_name = request.form.get('cameraName')
    camera_code = request.form.get('cameraCode')
    camera_branch_id = request.form.get('cameraBranchId')

    camera_vo = CameraVO()
    camera_dao = CameraDAO()

    camera_vo.camera_id = camera_id
    camera_vo.camera_name = camera_name
    camera_vo.camera_code = camera_code
    camera_vo.Camera_branch_id = camera_branch_id
    camera_dao.update_camera(camera_vo)

    return redirect('/admin/view_camera')

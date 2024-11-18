from flask import render_template, request, redirect

from base import app
from base.com.dao.branch_dao import BranchDAO
from base.com.vo.branch_vo import BranchVO


@app.route("/load_branch")
def branch():
    return render_template("admin/addBranch.html")


@app.route('/admin/add_branch', methods=['POST'])
def admin_insert_branch():
    branch_name = request.form.get('branchName')
    branch_address = request.form.get('branchAddress')
    branch_contact = request.form.get('branchContact')
    branch_manager = request.form.get('branchManager')

    branch_vo = BranchVO()
    branch_dao = BranchDAO()

    branch_vo.branch_name = branch_name
    branch_vo.branch_address = branch_address
    branch_vo.branch_contact = branch_contact
    branch_vo.branch_manager = branch_manager

    branch_dao.insert_branch(branch_vo)
    return redirect('/admin/view_branch')
    # return render_template("admin/home.html")


@app.route('/admin/view_branch')
def admin_view_branch():
    branch_dao = BranchDAO()
    branch_vo_list = branch_dao.view_branch()
    print('branch_vo_list', branch_vo_list)
    return render_template('admin/viewBranch.html',
                           branch_vo_list=branch_vo_list)


@app.route('/admin/delete_branch')
def admin_delete_branch():
    branch_vo = BranchVO()
    branch_dao = BranchDAO()
    branch_id = request.args.get('branchId')
    branch_vo.branch_id = branch_id
    branch_dao.delete_branch(branch_vo)
    return redirect('/admin/view_branch')


@app.route('/admin/edit_branch', methods=['GET'])
def admin_edit_branch():
    branch_vo = BranchVO()
    branch_dao = BranchDAO()

    branch_id = request.args.get('branchId')
    branch_vo.branch_id = branch_id
    branch_vo_list = branch_dao.edit_branch(branch_vo)
    return render_template('admin/editBranch.html',
                           branch_vo_list=branch_vo_list)


@app.route('/admin/update_branch', methods=['POST'])
def admin_update_branch():
    branch_id = request.form.get('branchId')
    branch_name = request.form.get('branchName')
    branch_address = request.form.get('branchAddress')
    branch_contact = request.form.get('branchContact')
    branch_manager = request.form.get('branchManager')

    branch_vo = BranchVO()
    branch_dao = BranchDAO()

    branch_vo.branch_id = branch_id
    branch_vo.branch_name = branch_name
    branch_vo.branch_address = branch_address
    branch_vo.branch_contact = branch_contact
    branch_vo.branch_manager = branch_manager
    branch_dao.update_branch(branch_vo)

    return redirect('/admin/view_branch')

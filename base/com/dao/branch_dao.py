from base import db
from base.com.vo.branch_vo import BranchVO


class BranchDAO:
    def insert_branch(self, branch_vo):
        db.session.add(branch_vo)
        db.session.commit()

    def view_branch(self):
        branch_vo_list = BranchVO.query.all()
        return branch_vo_list

    def delete_branch(self, branch_vo):
        branch_vo_list = BranchVO.query.get(branch_vo.branch_id)
        db.session.delete(branch_vo_list)
        db.session.commit()

    def edit_branch(self, branch_vo):
        branch_vo_list = BranchVO.query. \
            filter_by(branch_id=branch_vo.branch_id).all()
        return branch_vo_list

    def update_branch(self, branch_vo):
        db.session.merge(branch_vo)
        db.session.commit()

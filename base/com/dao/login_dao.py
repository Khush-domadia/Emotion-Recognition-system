from base import db
from base.com.vo.login_vo import LoginVO


class LoginDAO:

    def insert_login(self, login_vo):
        db.session.add(login_vo)
        db.session.commit()

    def view_login(self):
        login_vo_list = LoginVO.query.all()
        return login_vo_list

    def check_login_email(self, login_vo):
        login_vo_list = LoginVO.query.filter_by(
            login_email=login_vo.login_email).all()
        return login_vo_list

    def update_login(self, login_vo):
        db.session.merge(login_vo)
        db.session.commit()

    def find_login_id(self, login_vo):
        login_vo_list = \
            LoginVO.query.filter_by(
                login_email=login_vo.login_email).all()[
                -1].login_id
        return login_vo_list

    def login_validate_email(self, login_vo):
        login_vo_list = LoginVO.query.filter_by(
            login_email=login_vo.login_email).all()
        return login_vo_list

    def login_validate_password(self, login_vo):
        login_vo_list = LoginVO.query.filter_by(
            login_password=login_vo.login_password).all()
        return login_vo_list
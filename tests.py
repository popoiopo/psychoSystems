# tests.py

import os
import unittest
from flask import abort, url_for
from flask_testing import TestCase

from app import create_app, db
from app.models import Title, Temp_aspect, Temp_imp, Affiliation, Accepted, Expert


class TestBase(TestCase):

    def create_app(self):

        # pass in test configurations
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='mysql://psychoSystems_admin:Psycho1!@localhost/psychoSystems_test'
        )
        return app

    def setUp(self):
        """
        Will be called before every test
        """

        db.create_all()

        # create test admin user
        admin = Expert(username="psychoSystems_admin", password="Psycho1!", is_admin=True)

        # create test non-admin user
        expert = Expert(username="test_user", password="test2019")

        # save users to database
        db.session.add(admin)
        db.session.add(expert)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()


class TestModels(TestBase):

    def test_expert_model(self):
        """
        Test number of records in expert table
        """
        self.assertEqual(Expert.query.count(), 2)

    def test_accepted_model(self):
        """
        Test number of records in accepted table
        """

        # create test accepted
        accepted = Accepted(name="Meteen", description="Beste expert ooit")

        # save accepted to database
        db.session.add(accepted)
        db.session.commit()

        self.assertEqual(accepted.query.count(), 1)

    def test_title_model(self):
        """
        Test number of records in title table
        """

        # create test role
        title = Title(name="BerendBotje")

        # save role to database
        db.session.add(title)
        db.session.commit()

        self.assertEqual(title.query.count(), 1)


    def test_temp_aspect_model(self):
        """
        Test number of records in temp_aspect table
        """

        # create test role
        temp_aspect = Temp_aspect(name="Urenn")

        # save role to database
        db.session.add(temp_aspect)
        db.session.commit()

        self.assertEqual(temp_aspect.query.count(), 1)

    def test_temp_imp_model(self):
        """
        Test number of records in temp_imp table
        """

        # create test role
        temp_imp = Temp_imp(name="CEO")

        # save role to database
        db.session.add(temp_imp)
        db.session.commit()

        self.assertEqual(Temp_imp.query.count(), 1)

    def test_affiliation_model(self):
        """
        Test number of records in Affiliation table
        """

        # create test role
        affiliation = Affiliation(name="CEO")

        # save role to database
        db.session.add(affiliation)
        db.session.commit()

        self.assertEqual(Affiliation.query.count(), 1)


class TestViews(TestBase):

    def test_homepage_view(self):
        """
        Test that homepage is accessible without login
        """
        response = self.client.get(url_for('home.homepage'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        """
        Test that login page is accessible without login
        """
        response = self.client.get(url_for('auth.login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        """
        Test that logout link is inaccessible without login
        and redirects to login page then to logout
        """
        target_url = url_for('auth.logout')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_dashboard_view(self):
        """
        Test that dashboard is inaccessible without login
        and redirects to login page then to dashboard
        """
        target_url = url_for('home.dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_admin_dashboard_view(self):
        """
        Test that dashboard is inaccessible without login
        and redirects to login page then to dashboard
        """
        target_url = url_for('home.admin_dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_accepteds_view(self):
        """
        Test that accepteds page is inaccessible without login
        and redirects to login page then to accepteds page
        """
        target_url = url_for('admin.list_accepteds')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_temp_aspects_view(self):
        """
        Test that roles page is inaccessible without login
        and redirects to login page then to roles page
        """
        target_url = url_for('admin.list_temp_aspects')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_titles_view(self):
        """
        Test that roles page is inaccessible without login
        and redirects to login page then to roles page
        """
        target_url = url_for('admin.list_titles')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_affiliations_view(self):
        """
        Test that roles page is inaccessible without login
        and redirects to login page then to roles page
        """
        target_url = url_for('admin.list_affiliations')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_temp_imps_view(self):
        """
        Test that roles page is inaccessible without login
        and redirects to login page then to roles page
        """
        target_url = url_for('admin.list_temp_imps')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_temp_aspects_view(self):
        """
        Test that roles page is inaccessible without login
        and redirects to login page then to roles page
        """
        target_url = url_for('admin.list_affiliations')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_experts_view(self):
        """
        Test that experts page is inaccessible without login
        and redirects to login page then to experts page
        """
        target_url = url_for('admin.list_experts')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)


class TestErrorPages(TestBase):

    def test_403_forbidden(self):
        # create route to abort the request with the 403 Error
        @self.app.route('/403')
        def forbidden_error():
            abort(403)

        response = self.client.get('/403')
        self.assertEqual(response.status_code, 403)
        self.assertTrue("403 Error" in response.data)

    def test_404_not_found(self):
        response = self.client.get('/nothinghere')
        self.assertEqual(response.status_code, 404)
        self.assertTrue("404 Error" in response.data)

    def test_500_internal_server_error(self):
        # create route to abort the request with the 500 Error
        @self.app.route('/500')
        def internal_server_error():
            abort(500)

        response = self.client.get('/500')
        self.assertEqual(response.status_code, 500)
        self.assertTrue("500 Error" in response.data)


if __name__ == '__main__':
    unittest.main()
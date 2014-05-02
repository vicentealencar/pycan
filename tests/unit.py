import unittest
import pycan

from mock import Mock, patch


class PyCanTestCase(unittest.TestCase):
    def setUp(self):
        pycan._permissions = {}

    def get_basic_permission_params(self):
        return 'action', 'context', lambda u, r, c: True

    def get_full_permission_params(self):
        action, context, auth = self.get_basic_permission_params()
        return action, context, auth, lambda _, __: True, lambda _, __: True

    def get_basic_context(self):
        return {
            'location': 'middle earth',
            'era': 3
        }

    def assert_action_was_stored(self, action, context, auth):
        self.assertIn(context, pycan._permissions)
        self.assertIn(action, pycan._permissions[context])
        self.assertEqual(pycan._permissions[context][action]['authorization'], auth)

    def assert_mutiple_actions_were_stored(self, action_set, context, auth):
        for action in action_set:
            self.assert_action_was_stored(action, context, auth)


class CanTest(PyCanTestCase):
    def test_can_repeated_single_action(self):
        action, context, auth = self.get_basic_permission_params()
        pycan.can(action, context, auth)
        self.assertRaises(pycan.exceptions.ActionAlreadyExistsError, pycan.can, action, context, auth)

    def test_can_repeated_multiple_action(self):
        action, context, auth = self.get_basic_permission_params()
        action_set = [action, 'actionA', 'actionB']
        pycan.can(action_set, context, auth)
        self.assertRaises(pycan.exceptions.ActionAlreadyExistsError, pycan.can, action, context, auth)

    def test_can_single_action_single_context(self):
        action, context, auth = self.get_basic_permission_params()
        pycan.can(action, context, auth)
        self.assert_action_was_stored(action, context, auth)

    def test_can_single_action_multiple_contexts(self):
        action, _, auth = self.get_basic_permission_params()
        context_set = ['contextOne', 'contextTwo', 'contextThree']
        pycan.can(action, context_set, auth)
        for context in context_set:
            self.assert_action_was_stored(action, context, auth)

    def test_can_multiple_actions_single_context(self):
        _, context, auth = self.get_basic_permission_params()
        action_set = ['actionOne', 'actionTwo', 'actionThree']
        pycan.can(action_set, context, auth)
        self.assert_mutiple_actions_were_stored(action_set, context, auth)

    def test_can_multiple_actions_multiple_contexts(self):
        _, _, auth = self.get_basic_permission_params()
        action_set = ['actionOne', 'actionTwo', 'actionThree']
        context_set = ['contextOne', 'contextTwo', 'contextThree']
        pycan.can(action_set, context_set, auth)
        for context in context_set:
            self.assert_mutiple_actions_were_stored(action_set, context, auth)

    def test_can_asterisk_in_action_set(self):
        _, context, auth = self.get_basic_permission_params()
        action_set = ['actionA', '*']
        self.assertRaises(pycan.exceptions.ActionListWithAsteriskError, pycan.can, action_set, context, auth)

    def test_can_asterisk_in_context_with_action(self):
        action, context, auth = self.get_basic_permission_params()
        pycan.can(action, context, auth)
        self.assertRaises(pycan.exceptions.ContextAlreadyHasActionsError, pycan.can, '*', context, auth)

    def test_can_asterisk_action_in_context_with_asterisk(self):
        action, context, auth = self.get_basic_permission_params()
        pycan.can('*', context, auth)
        self.assertRaises(pycan.exceptions.ContextAlreadyHasAsteriskError, pycan.can, action, context, auth)

    def test_authorization_param_validation(self):
        with patch('pycan._assert_authorization_parameters') as assert_parameters:
            self.test_can_single_action_single_context()
            self.assertEquals(assert_parameters.call_count, 1)

    def test_can_authorization(self):
        pass

    def test_can_load_before(self):
        pass

    def test_can_load_after(self):
        pass

class CanITest(PyCanTestCase):
    def test_can_i_false_result(self):
        pass

    def test_can_i_true_result(self):
        pass


class AuthorizeTest(PyCanTestCase):
    def test_authorize_sucess(self):
        action, context, _, get_auth_resource, load_after = self.get_full_permission_params()
        auth = lambda user, context, resource: user == 'gandalf' and context['location'] == 'middle earth'
        pycan.can(action, context, auth, get_auth_resource, load_after)
        auth_resource, resource = pycan.authorize(action, context, 'gandalf', self.get_basic_context())
        self.assertTrue(auth_resource)
        self.assertTrue(resource)

    def test_authorize_fail(self):
        action, context, _, get_auth_resource, load_after = self.get_full_permission_params()
        auth = lambda user, context, resource: user == 'gandalf' and context['location'] == 'middle earth'
        pycan.can(action, context, auth, get_auth_resource, load_after)
        self.assertRaises(pycan.exceptions.UnauthorizedResourceError, pycan.authorize, action, context, 'elrond',
                          self.get_basic_context())

    def test_authorize_with_missing_context(self):
        action, context, auth = self.get_basic_permission_params()
        pycan.can(action, context, auth)
        self.assertRaises(pycan.exceptions.UnauthorizedResourceError, pycan.authorize, action, 'no_context', 'gandalf',
                          self.get_basic_context())

    def test_authorize_with_missing_action(self):
        action, context, auth = self.get_basic_permission_params()
        pycan.can(action, context, auth)
        self.assertRaises(pycan.exceptions.UnauthorizedResourceError, pycan.authorize, 'no_action', context, 'gandalf',
                          self.get_basic_context())

    def test_authorize_custom_exception_action(self):
        class CustomException(Exception):
            def __init__(self, **kwargs):
                pass

        action, context, _ = self.get_basic_permission_params()
        pycan.can(action, context, lambda u, r, c: False, exception = CustomException)
        self.assertRaises(CustomException, pycan.authorize, action, context, 'gandalf',
                          self.get_basic_context())

    def test_authorize_asterisk_action(self):
        _, context, auth = self.get_basic_permission_params()
        pycan.can('*', context, auth)
        app_context = self.get_basic_context()
        try:
            pycan.authorize('foo', context, app_context)
        except Exception:
            self.fail("authorize raised UnauthorizedResourceError")


class ExceptionTest(PyCanTestCase):

    def test_custom_exception_per_method_is_thrown(self):
        class CustomException(Exception):
            def __init__(self, **kwargs):
                pass 

        def custom_auth(u, c, r):
            raise CustomException()

        action, context, _ = self.get_basic_permission_params()
        pycan.can(action, context, custom_auth)        
        self.assertRaises(CustomException, pycan.authorize, action, context, 'gandalf',
                          self.get_basic_context())

class ExtrasTest(PyCanTestCase):
    def test_combine_with_or(self):
        test_function = pycan.or_(
            lambda u, c, r: u == c,
            lambda u, c, r: u == r,
            lambda u, c, r: c == r)

        self.assertTrue(test_function(1, 1, 1))
        self.assertTrue(test_function(1, 1, 0))
        self.assertTrue(test_function(1, 0, 1))
        self.assertTrue(test_function(0, 1, 1))
        self.assertFalse(test_function(1, 2, 3))

    def test_combine_with_and(self):
        test_function = pycan.and_(
            lambda u, c, r: u == c,
            lambda u, c, r: u == r,
            lambda u, c, r: c == r)

        self.assertTrue(test_function(1, 1, 1))
        self.assertFalse(test_function(1, 1, 0))
        self.assertFalse(test_function(1, 0, 1))
        self.assertFalse(test_function(0, 1, 1))
        self.assertFalse(test_function(1, 2, 3))

    def test_combine_with_not(self):
        self.assertTrue(pycan.not_(lambda u, c, r: False)(None, None, None))
        self.assertFalse(pycan.not_(lambda u, c, r: True)(None, None, None))

    def test_not_param_validation(self):
        with patch('pycan._assert_authorization_parameters') as assert_parameters:
            self.test_combine_with_not()
            self.assertEquals(assert_parameters.call_count, 2)

    def test_or_is_lazy(self):
        with patch('pycan._assert_authorization_parameters') as assert_parameters:
            assert_parameters.return_value = True
            test_functions = [Mock(), Mock(), Mock()]
            combined_function = pycan.or_(*test_functions)

            test_functions[0].return_value = True
            combined_function(1, 1, 3)
            test_functions[0].assert_called_once_with(1, 1, 3)
            self.assertEquals(test_functions[1].call_count, 0)
            self.assertEquals(test_functions[2].call_count, 0)

            test_functions[0].return_value = False
            test_functions[1].return_value = True
            combined_function(2, 1, 2)
            self.assertEquals(test_functions[0].call_count, 2)
            test_functions[1].assert_called_once_with(2, 1, 2)
            self.assertEquals(test_functions[2].call_count, 0)

            test_functions[0].return_value = False
            test_functions[1].return_value = False
            test_functions[2].return_value = True
            combined_function(1, 2, 2)
            self.assertEquals(test_functions[0].call_count, 3)
            self.assertEquals(test_functions[1].call_count, 2)
            test_functions[2].assert_called_once_with(1, 2, 2)

    def test_and_is_lazy(self):
        with patch('pycan._assert_authorization_parameters') as assert_parameters:
            assert_parameters.return_value = True
            test_functions = [Mock(), Mock(), Mock()]
            combined_function = pycan.and_(*test_functions)

            test_functions[0].return_value = False
            combined_function(1, 2, 1)
            test_functions[0].assert_called_once_with(1, 2, 1)
            self.assertEquals(test_functions[1].call_count, 0)
            self.assertEquals(test_functions[2].call_count, 0)

            test_functions[0].return_value = True
            test_functions[1].return_value = False
            combined_function(1, 1, 2)
            self.assertEquals(test_functions[0].call_count, 2)
            test_functions[1].assert_called_once_with(1, 1, 2)
            self.assertEquals(test_functions[2].call_count, 0)

            test_functions[0].return_value = True
            test_functions[1].return_value = True
            test_functions[2].return_value = True
            combined_function(2, 2, 2)
            self.assertEquals(test_functions[0].call_count, 3)
            self.assertEquals(test_functions[1].call_count, 2)
            test_functions[2].assert_called_once_with(2, 2, 2)

    def test_and_param_validation(self):
        self.assertRaises(AssertionError, pycan.and_)
        with patch('pycan._assert_authorization_parameters') as assert_params:
            self.test_combine_with_and()
            self.assertEquals(assert_params.call_count, 3)

    def test_or_param_validation(self):
        self.assertRaises(AssertionError, pycan.or_)
        with patch('pycan._assert_authorization_parameters') as assert_params:
            self.test_combine_with_or()
            self.assertEquals(assert_params.call_count, 3)

    def test_assert_authorization_params(self):
        self.assertRaises(AssertionError, pycan._assert_authorization_parameters, None)
        self.assertRaises(AssertionError, pycan._assert_authorization_parameters, lambda u, c: True)
        pycan._assert_authorization_parameters(lambda u, c, r: True)

    def test_is_sequence_is_true(self):
        self.assertTrue(pycan._is_sequence(['A','B','C','D']))
        self.assertTrue(pycan._is_sequence(('A','B','C','D')))

    def test_is_sequence_is_false(self):
        self.assertFalse(pycan._is_sequence('ABCD'))
        self.assertFalse(pycan._is_sequence(12345))

    def test_allow_to_all(self):
        context = self.get_basic_context()
        self.assertTrue(pycan.allow_to_all('gandalf',context, {'foo':'bar'}))

    def test_revoke(self):
        pycan.can('a', 'b', pycan.allow_to_all)
        try:
            auth_resource, _ = pycan.authorize('a', 'b', 'gandalf', self.get_basic_context())
        except Exception:
            self.fail("authorize raised UnauthorizedResourceError")

        pycan.revoke('a', 'b')
        self.assertRaises(pycan.exceptions.UnauthorizedResourceError, pycan.authorize, 'a', 'b', 'elrond',
                          self.get_basic_context())




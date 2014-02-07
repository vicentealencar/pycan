import unittest
import pycan

class PyCanTestCase(unittest.TestCase):
    def setUp(self):
        pycan._permissions = {}

    def get_basic_permission_params(self):
        return 'action', 'target', lambda u, r, c: True

    def get_full_permission_params(self):
        action, target, auth = self.get_basic_permission_params()
        return action, target, auth, lambda _,__: True, lambda _,__: True

    def assert_action_was_stored(self, action, target, auth):
        self.assertIn(target, pycan._permissions)
        self.assertIn(action, pycan._permissions[target])
        self.assertEqual(pycan._permissions[target][action]['authorization'], auth)

    def assert_mutiple_actions_were_stored(self, action_set, target, auth):
        for action in action_set:
            self.assert_action_was_stored(action, target, auth)


class CanTest(PyCanTestCase):
    def test_can_repeated_single_action(self):
        action, target, auth = self.get_basic_permission_params()
        pycan.can(action, target, auth)
        self.assertRaises(pycan.exceptions.ActionAlreadyExistsError, pycan.can, action, target, auth)

    def test_can_repeated_multiple_action(self):
        action, target, auth = self.get_basic_permission_params()
        action_set = [action, 'actionA', 'actionB']
        pycan.can(action_set, target, auth)
        self.assertRaises(pycan.exceptions.ActionAlreadyExistsError, pycan.can, action, target, auth)        

    def test_can_single_action_single_target(self):
        action, target, auth = self.get_basic_permission_params()
        pycan.can(action, target, auth)
        self.assert_action_was_stored(action, target, auth)

    def test_can_single_action_multiple_targets(self):
        action, _, auth = self.get_basic_permission_params()
        target_set = ['targetOne', 'targetTwo', 'targetThree']
        pycan.can(action, target_set, auth)
        for target in target_set:
            self.assert_action_was_stored(action, target, auth)

    def test_can_multiple_actions_single_target(self):
        _, target, auth = self.get_basic_permission_params()
        action_set = ['actionOne', 'actionTwo', 'actionThree']
        pycan.can(action_set, target, auth)
        self.assert_mutiple_actions_were_stored(action_set, target, auth)

    def test_can_multiple_actions_multiple_targets(self):
        _, _, auth = self.get_basic_permission_params()
        action_set = ['actionOne', 'actionTwo', 'actionThree']
        target_set = ['targetOne', 'targetTwo', 'targetThree']
        pycan.can(action_set, target_set, auth)
        for target in target_set:
            self.assert_mutiple_actions_were_stored(action_set, target, auth)

    def test_can_asterisk_in_action_set(self):
        _, target, auth = self.get_basic_permission_params()
        action_set = ['actionA', '*']
        self.assertRaises(pycan.exceptions.ActionListWithAsteriskError, pycan.can, action_set, target, auth)

    def test_can_asterisk_in_target_with_action(self):
        action, target, auth = self.get_basic_permission_params()
        pycan.can(action, target, auth)
        self.assertRaises(pycan.exceptions.TargetAlreadyHasActionsError, pycan.can, '*', target, auth)

    def test_can_asterisk_action_in_target_with_asterisk(self):
        action, target, auth = self.get_basic_permission_params()
        pycan.can('*', target, auth)
        self.assertRaises(pycan.exceptions.TargetAlreadyHasAsteriskError, pycan.can, action, target, auth)

    def test_can_authorization(self):
        pass

    def test_can_get_authorization_resource(self):
        pass

    def test_can_get_resource(self):
        pass

class CanITest(PyCanTestCase):    
    def test_can_i_false_result(self):    
        pass       

    def test_can_i_true_result(self):
        pass
  

class AuthorizeTest(PyCanTestCase):
    def get_basic_context(self):
        return {
            'location':'middle earth',
            'era': 3
        }

    def test_authorize_sucess(self):
        action, target, _, get_auth_resource, get_resource = self.get_full_permission_params()
        auth = lambda user, context, resource: user == 'gandalf' and context['location'] == 'middle earth'
        pycan.can(action, target, auth, get_auth_resource, get_resource)
        auth_resource, resource = pycan.authorize(action, target, 'gandalf', self.get_basic_context())
        self.assertTrue(auth_resource)
        self.assertTrue(resource)
    
    def test_authorize_fail(self):
        action, target, _, get_auth_resource, get_resource = self.get_full_permission_params()
        auth = lambda user, context, resource: user == 'gandalf' and context['location'] == 'middle earth'
        pycan.can(action, target, auth, get_auth_resource, get_resource)
        self.assertRaises(pycan.exceptions.UnauthorizedResourceError, pycan.authorize, action, target, 'elrond', self.get_basic_context())        

    def test_authorize_with_missing_target(self):
        action, target, auth = self.get_basic_permission_params()
        pycan.can(action, target, auth)
        self.assertRaises(pycan.exceptions.UnauthorizedResourceError, pycan.authorize, action, 'no_target', 'gandalf', self.get_basic_context())

    def test_authorize_with_missing_action(self):
        action, target, auth = self.get_basic_permission_params()
        pycan.can(action, target, auth)
        self.assertRaises(pycan.exceptions.UnauthorizedResourceError, pycan.authorize, 'no_action', target, 'gandalf', self.get_basic_context())


class ExtrasTest(unittest.TestCase):

    def test_is_sequence_is_true(self):
        self.assertTrue(pycan._is_sequence(['A','B','C','D']))
        self.assertTrue(pycan._is_sequence(('A','B','C','D')))
      
    def test_is_sequence_is_false(self):
        self.assertFalse(pycan._is_sequence('ABCD'))
        self.assertFalse(pycan._is_sequence(12345))

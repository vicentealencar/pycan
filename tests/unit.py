import unittest
import pycan

class CanTest(unittest.TestCase):
    def setUp(self):
        pycan._permissions = {}

    def get_basic_permission_params(self):
        return 'action', 'target', lambda u, r, c: True

    def assert_action_was_stored(self, action, target, auth):
        self.assertIn(target, pycan._permissions)
        self.assertIn(action, pycan._permissions[target])
        self.assertEqual(pycan._permissions[target][action]['authorization'], auth)

    def assert_mutiple_actions_were_stored(self, action_set, target, auth):
        for action in action_set:
            self.assert_action_was_stored(action, target, auth)

    def can_repeated_single_action_test(self):
        action, target, auth = self.get_basic_permission_params()
        pycan.can(action, target, auth)
        self.assertRaises(pycan.exceptions.ActionAlreadyExistsError, pycan.can, action, target, auth)

    def can_repeated_multiple_action_test(self):
        action, target, auth = self.get_basic_permission_params()
        action_set = [action, 'actionA', 'actionB']
        pycan.can(action_set, target, auth)
        self.assertRaises(pycan.exceptions.ActionAlreadyExistsError, pycan.can, action, target, auth)        

    def can_single_action_single_target_test(self):
        action, target, auth = self.get_basic_permission_params()
        pycan.can(action, target, auth)
        self.assert_action_was_stored(action, target, auth)

    def can_single_action_multiple_targets_test(self):
        action, _, auth = self.get_basic_permission_params()
        target_set = ['targetOne', 'targetTwo', 'targetThree']
        pycan.can(action, target_set, auth)
        for target in target_set:
            self.assert_action_was_stored(action, target, auth)

    def can_multiple_actions_single_target_test(self):
        _, target, auth = self.get_basic_permission_params()
        action_set = ['actionOne', 'actionTwo', 'actionThree']
        pycan.can(action_set, target, auth)
        self.assert_mutiple_actions_were_stored(action_set, target, auth)

    def can_multiple_actions_multiple_targets_test(self):
        _, _, auth = self.get_basic_permission_params()
        action_set = ['actionOne', 'actionTwo', 'actionThree']
        target_set = ['targetOne', 'targetTwo', 'targetThree']
        pycan.can(action_set, target_set, auth)
        for target in target_set:
            self.assert_mutiple_actions_were_stored(action_set, target, auth)

    def can_asterisk_in_action_set_test(self):
        _, target, auth = self.get_basic_permission_params()
        action_set = ['actionA', '*']
        self.assertRaises(pycan.exceptions.ActionListWithAsteriskError, pycan.can, action_set, target, auth)

    def can_asterisk_in_target_with_action_test(self):
        action, target, auth = self.get_basic_permission_params()
        pycan.can(action, target, auth)
        self.assertRaises(pycan.exceptions.TargetAlreadyHasActionsError, pycan.can, '*', target, auth)

    def can_asterisk_action_in_target_with_asterisk_test(self):
        action, target, auth = self.get_basic_permission_params()
        pycan.can('*', target, auth)
        self.assertRaises(pycan.exceptions.TargetAlreadyHasAsteriskError, pycan.can, action, target, auth)

    def can_authorization_test(self):
        pass

    def can_get_authorization_resource_test(self):
        pass

    def can_get_resource_test(self):
        pass

    def can_exception_test(self):
        pass


class CanITest(unittest.TestCase):
    def setUp(self):
        pass


class AuthorizeTest(unittest.TestCase):
    def setUp(self):
        pass

    def get_basic_authorization(self):
        pass

    def authorize_sucess_test(self):

        pass
    
    def authorize_fail_test(self):
        pass

    def authorize_with_missing_target_test(self):
        pass

    def authorize_with_missing_action_test(self):
        pass


class ExtrasTest(unittest.TestCase):

    def is_sequence_is_true_test(self):
        self.assertTrue(pycan._is_sequence(['A','B','C','D']))
        self.assertTrue(pycan._is_sequence(('A','B','C','D')))
      
    def is_sequence_is_false_test(self):
        self.assertFalse(pycan._is_sequence('ABCD'))
        self.assertFalse(pycan._is_sequence(12345))

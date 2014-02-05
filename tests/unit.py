import unittest
import pycan

class CanTest(unittest.TestCase):
  def setUp(self):
    pycan._permissions = {}

  def can_no_target_test(self):
    pass

  def can_single_target_test(self):
    pass

  def can_array_targets_test(self):
    pass

  def can_no_action_test(self):
    pass

  def assert_action_was_stored(self, action, target, auth):
    self.assertIn(target, pycan._permissions)
    self.assertIn(action, pycan._permissions[target])
    self.assertEqual(pycan._permissions[target][action]['authorization'], auth)

  def can_single_action_test(self):
    target = 'target'
    action = 'action'
    auth = lambda u, r, c: True
    pycan.can(action, target, auth)
    self.assert_action_was_stored(action, target, auth)

    targets = ['targetOne', 'targetTwo', 'targetThree']
    pycan.can(action, targets, auth)
    for target in targets:
      self.assert_action_was_stored(action, target, auth)

  def can_array_actions_test(self):
    target = 'target'
    actions = ['actionOne', 'actionTwo', 'actionThree']
    auth = lambda u, r, c: True
    pycan.can(actions, target, auth)
    for action in actions:
      self.assert_action_was_stored(action, target, auth)

    targets = ['targetOne', 'targetTwo', 'targetThree']
    pycan.can(actions, targets, auth)
    for target in targets:
      for action in actions:
        self.assert_action_was_stored(action, target, auth)

  def can_asterisk_test(self):
    target = 'target'
    actions = ['actionA','*']
    auth = lambda u, r, c: True
    self.assertRaises(pycan.exceptions.ActionListWithAsteriskError, pycan.can, actions, target, auth)

    pycan.can('action', target, auth)
    self.assertRaises(pycan.exceptions.TargetAlreadyHasActionsError, pycan.can, '*', target, auth)

    target = 'targetTwo'
    pycan.can('*', target, auth)
    self.assertRaises(pycan.exceptions.TargetAlreadyHasAsteriskError, pycan.can, 'action', target, auth)


  def can_authorization_test(self):
    pass

  def can_get_authorization_resource_test(self):
    pass

  def can_get_resource_test(self):
    pass

  def can_exception_test(self):
    pass

  def can_full_test(self):
    pass

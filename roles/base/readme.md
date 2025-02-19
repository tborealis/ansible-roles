The sshd config is altered by this role. To prevent any handlers after sshd failing due to the config change a handler 
has not been created to restart sshd. You need to add `post-tasks.yml` to the `post_tasks` section of your play:

```
post_tasks:
- ansible.builtin.import_tasks: roles/base/tasks/post-tasks.yml
```

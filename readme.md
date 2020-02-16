# 云班课接口

- [x] 登录
- [x] 保存登录状态
- [x] 获取课程列表
- [x] 获取打卡列表
- [x] 获取任务列表
- [x] 获取班级成员列表
- [x] 签到
- [ ] 获取资源列表
- [ ] 获取活动列表和参与活动 

## 使用方法

```python
from yunbanke.user import User
u = User()
u.login_user("user","pwd")
print(u.list_course())
```
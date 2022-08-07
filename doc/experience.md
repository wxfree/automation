> Charles
### Failed to install helper CFErrorDomainLaunchd error 9解决方案
1. `launchctl print-disabled system` 回车后查看`com.xk72.charles.ProxyHelper`这一项后面是true就进行下一步
2. `sudo launchctl enable system/com.xk72.charles.ProxyHelper`，按回车，然后正确输入系统密码即可
3. 重启Charles



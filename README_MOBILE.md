# 燧石Agent移动端应用

## 概述

燧石Agent的React Native移动端应用，支持Android平台。

## 功能特性

### 四大核心模块

1. **首页**
   - 系统介绍和能力展示
   - 架构说明

2. **智能客服监控** (Level 1)
   - 对话实时分析
   - 情绪和意图识别
   - 智能预警触发
   - 推荐措施生成

3. **小红书创作** (Level 2)
   - 爆款笔记分析
   - 内容策略规划
   - 智能文案生成
   - 标签推荐

4. **产品经理** (Level 3)
   - 需求输入
   - PRD文档生成
   - 痛点分析
   - 功能设计

5. **设置**
   - API配置
   - 应用偏好设置
   - 版本信息

## 快速开始

### 1. 安装依赖

```bash
cd mobile
npm install
```

### 2. 启动开发服务器

```bash
npm start
```

### 3. 运行应用

**Android设备/模拟器：**
```bash
npm run android
```

## 打包APK

### Windows系统

```bash
# 在项目根目录运行
build-android.bat
```

### Linux/Mac系统

```bash
# 在项目根目录运行
./build-android.sh
```

## 技术栈

- **React Native 0.73**：跨平台移动应用框架
- **React Navigation**：路由和导航
- **React Native Paper**：Material Design组件库
- **Axios**：HTTP客户端
- **AsyncStorage**：本地持久化存储

## 项目结构

```
mobile/
├── android/                 # Android原生代码
│   ├── app/                # 应用模块
│   │   └── src/main/       # 主要源代码
│   ├── build.gradle        # 项目级构建配置
│   └── gradlew             # Gradle包装器
├── src/
│   ├── screens/            # 页面组件
│   │   ├── HomeScreen.tsx
│   │   ├── MonitorScreen.tsx
│   │   ├── RedNoteScreen.tsx
│   │   ├── ProductScreen.tsx
│   │   └── SettingsScreen.tsx
│   └── App.tsx             # 应用入口
├── package.json
├── app.json
└── babel.config.js
```

## 配置说明

### API配置

在"设置"页面配置：
- API提供商（Qwen/DeepSeek/GLM）
- API Key
- 推送通知
- 深色模式

### 环境变量

可以创建 `.env` 文件配置：
```
REACT_NATIVE_APP_API_BASE_URL=http://your-server.com/api
REACT_NATIVE_APP_API_KEY=your_api_key
```

## 后端集成

移动端通过API与后端服务通信：

```typescript
// 示例API调用
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://your-server.com/api',
  timeout: 30000,
});

// 调用客服监控API
const response = await api.post('/monitor/analyze', {
  userQuery: '...',
  aiResponse: '...',
  systemState: {...}
});
```

## 构建配置

### 签名密钥

应用使用自动生成的调试密钥。生产发布需要：
1. 生成正式签名密钥
2. 配置 `android/app/build.gradle`
3. 配置 `android/gradle.properties`

详细配置见 `BUILD_ANDROID.md`

## 常见问题

### Gradle构建失败

**解决方案：**
```bash
cd android
./gradlew clean
./gradlew assembleRelease
```

### 无法连接到Metro bundler

**解决方案：**
```bash
adb reverse tcp:8081 tcp:8081
npm start
```

### APK安装失败

**检查：**
1. 是否启用了"未知来源"安装
2. Android版本是否兼容
3. 签名是否正确

## 发布到应用商店

1. **准备材料**
   - 应用图标（多尺寸）
   - 应用截图
   - 应用描述
   - 隐私政策

2. **构建发布版本**
   - 使用正式签名
   - 生成AAB格式（推荐）
   - 或APK格式

3. **提交审核**
   - 上传到Google Play
   - 填写应用信息
   - 等待审核通过

## 性能优化

- 使用Hermes引擎
- 启用ProGuard混淆
- 优化图片资源
- 使用Bundle分割

## 安全建议

- 不要在代码中硬编码API Key
- 使用HTTPS通信
- 实施证书绑定
- 加密敏感数据

## 更新日志

### v1.0.0 (2024-01-09)
- 初始版本发布
- 实现四大核心功能
- 支持Android平台

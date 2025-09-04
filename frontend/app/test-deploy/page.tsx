export default function TestDeployPage() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-3xl font-bold mb-4">部署测试页面</h1>
        <p className="text-lg mb-2">如果你能看到这个页面，说明部署成功了</p>
        <p className="text-sm text-gray-600">部署时间: {new Date().toISOString()}</p>
        <div className="mt-8 space-y-2">
          <p>
            <a href="/p/1001" className="text-blue-600 underline">
              访问新预测页面 /p/1001
            </a>
          </p>
          <p>
            <a href="/api-test" className="text-blue-600 underline">
              访问API测试页面 /api-test
            </a>
          </p>
          <p>
            <a href="/prediction/1001" className="text-blue-600 underline">
              访问原预测页面 /prediction/1001
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}
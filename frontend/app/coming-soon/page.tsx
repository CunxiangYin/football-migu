'use client';

import { useRouter } from 'next/navigation';
import { useSearchParams } from 'next/navigation';
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { AlertCircle, ArrowLeft, Rocket, Calendar, Bell } from 'lucide-react';

export default function ComingSoonPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const feature = searchParams.get('feature') || '该功能';

  const features = [
    { name: '实时比赛数据', icon: '📊', status: 'developing', progress: 70 },
    { name: '用户登录系统', icon: '👤', status: 'planned', progress: 30 },
    { name: '个人中心', icon: '⚙️', status: 'planned', progress: 20 },
    { name: '支付系统', icon: '💳', status: 'planned', progress: 10 },
    { name: '社区讨论', icon: '💬', status: 'planned', progress: 15 },
    { name: '数据分析', icon: '📈', status: 'developing', progress: 60 },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <Card className="max-w-2xl w-full shadow-2xl">
        <CardContent className="p-8">
          {/* 主要提示区域 */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-20 h-20 bg-orange-100 rounded-full mb-4">
              <Rocket className="w-10 h-10 text-orange-500" />
            </div>
            
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              功能即将上线
            </h1>
            
            <p className="text-lg text-gray-600 mb-4">
              <span className="font-semibold text-indigo-600">{feature}</span> 正在开发中
            </p>
            
            <div className="flex items-center justify-center gap-2 text-yellow-600 bg-yellow-50 px-4 py-2 rounded-lg inline-flex">
              <AlertCircle className="w-5 h-5" />
              <span className="text-sm font-medium">预计上线时间：2024年2月</span>
            </div>
          </div>

          {/* 功能开发进度 */}
          <div className="mb-8">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">开发进度</h2>
            <div className="space-y-3">
              {features.map((item, index) => (
                <div key={index} className="flex items-center gap-3">
                  <span className="text-2xl">{item.icon}</span>
                  <div className="flex-1">
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-sm font-medium text-gray-700">{item.name}</span>
                      <span className="text-xs text-gray-500">{item.progress}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full transition-all duration-500 ${
                          item.status === 'developing' ? 'bg-blue-500' : 'bg-gray-400'
                        }`}
                        style={{ width: `${item.progress}%` }}
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* 订阅提醒 */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <div className="flex items-start gap-3">
              <Bell className="w-5 h-5 text-blue-600 mt-0.5" />
              <div className="flex-1">
                <h3 className="font-medium text-blue-900 mb-1">获取上线通知</h3>
                <p className="text-sm text-blue-700 mb-3">
                  订阅后，我们将在功能上线时第一时间通知您
                </p>
                <div className="flex gap-2">
                  <input
                    type="email"
                    placeholder="请输入您的邮箱"
                    className="flex-1 px-3 py-2 border border-blue-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                    disabled
                  />
                  <Button
                    variant="default"
                    size="sm"
                    className="bg-blue-600 hover:bg-blue-700"
                    disabled
                  >
                    订阅
                  </Button>
                </div>
                <p className="text-xs text-blue-600 mt-2">* 订阅功能也在开发中 😊</p>
              </div>
            </div>
          </div>

          {/* 操作按钮 */}
          <div className="flex gap-3 justify-center">
            <Button
              variant="outline"
              onClick={() => router.back()}
              className="flex items-center gap-2"
            >
              <ArrowLeft className="w-4 h-4" />
              返回上一页
            </Button>
            
            <Button
              onClick={() => router.push('/')}
              className="bg-indigo-600 hover:bg-indigo-700 text-white"
            >
              返回首页
            </Button>
            
            <Button
              variant="outline"
              onClick={() => router.push('/demo.html')}
              className="flex items-center gap-2"
            >
              <Calendar className="w-4 h-4" />
              查看演示
            </Button>
          </div>

          {/* 底部说明 */}
          <div className="mt-8 pt-6 border-t border-gray-200">
            <p className="text-center text-sm text-gray-500">
              我们正在努力开发新功能，敬请期待！如有疑问，请联系 support@example.com
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
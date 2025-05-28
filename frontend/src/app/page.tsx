import Image from "next/image";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Tickets P2P
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            A peer-to-peer marketplace platform for event ticket reselling. 
            Connect ticket holders with potential buyers in a trusted environment.
          </p>
          <div className="space-y-4">
            <div className="bg-white rounded-lg shadow-md p-6 max-w-md mx-auto">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">
                Welcome to Tickets P2P
              </h2>
              <p className="text-gray-600">
                The platform is currently in development. Stay tuned for the launch!
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

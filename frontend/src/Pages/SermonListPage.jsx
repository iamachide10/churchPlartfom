
import SermonCard from "../Components/SermonCard"; 


export const SermonListPage  = () => {


  const sermons = [
    { preacher: "Pastor John Doe", title: "Walking in Faith", date: "Sept 20, 2025" },
    { preacher: "Rev. Mary Smith", title: "The Power of Prayer", date: "Sept 18, 2025" },
    { preacher: "Bishop Samuel", title: "Living with Purpose", date: "Sept 15, 2025" },
    { preacher: "Pastor Grace", title: "The Gift of Salvation", date: "Sept 10, 2025" },
    { preacher: "Rev. Paul Mensah", title: "Overcoming Temptation", date: "Sept 8, 2025" },
    { preacher: "Evangelist Sarah", title: "Love That Transforms", date: "Sept 5, 2025" },
    { preacher: "Pastor Daniel", title: "Hope in Hard Times", date: "Sept 2, 2025" },
    { preacher: "Rev. Kwame", title: "Faith That Moves Mountains", date: "Aug 30, 2025" },
    { preacher: "Pastor Lydia", title: "Serving God with Joy", date: "Aug 28, 2025" },
    { preacher: "Bishop Emmanuel", title: "God’s Plan for You", date: "Aug 25, 2025" },
  ];

  return (
    <div className="min-h-screen bg-gray-900 text-white px-4 sm:px-6 lg:px-12 py-10">
      {/* Page Title */}
      <h1 className="text-3xl font-bold text-yellow-400 mb-8 text-center">
        Sermons
      </h1>

      {/* Grid of Sermons */}
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {sermons.map((sermon, index) => (
          <SermonCard
            key={index}
            preacher={sermon.preacher}
            title={sermon.title}
            date={sermon.date}
          />
        ))}
      </div>
    </div>
  );
};



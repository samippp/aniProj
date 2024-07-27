import Navbar from "./Navbar";
import axios from "axios";
import { useEffect, useState, useCallback } from "react";
import { PieChart, Pie, Sector, ResponsiveContainer } from "recharts";
import AnimePanel from "./AnimePanel";
import {FaArrowCircleUp} from 'react-icons/fa'; 

export default function UserStats() {
  const [favouriteGenres, setFavouriteGenre] = useState([]);
  const [recommendedAnime, setRecommendedAnime] = useState([]);
  const [likedAnime, setLikedAnime] = useState([]);
  const [showXAmount, setXAmount] = useState(5);
  const [arrow, setVisibleArrow] = useState(false);

  function range(start, end) {
    return Array.from({ length: end - start }, (v, k) => k + start);
  }

  const toggleVisible = () => { 
    const scrolled = document.documentElement.scrollTop; 
    if (scrolled > 300){ 
      setVisibleArrow(true) 
    }  
    else if (scrolled <= 300){ 
      setVisibleArrow(false) 
    } 
  }; 

  window.addEventListener('scroll',toggleVisible);

const scrollToTop = () =>{ 
    window.scrollTo({ 
      top: 0,  
      behavior: 'smooth'
    }); 
}; 


  async function getFavouriteGenres() {
    axios
      .post("http://127.0.0.1:8000/api/favourite_genres/", {
        name: localStorage.getItem("email"),
      })
      .then((response) => {
        setFavouriteGenre([]);
        const keys = Object.keys(response.data[0]);
        for (let i = 0; i < keys.length; i++) {
          let key = keys[i];
          setFavouriteGenre((prev) => [
            ...prev,
            { name: key, value: response.data[0][key] },
          ]);
        }
      })
      .catch((error) => {
        console.log(error);
      });
  }

  async function getRecommended() {
    axios
      .post("http://127.0.0.1:8000/api/recommendations/", {
        name: localStorage.getItem("email"),
      })
      .then((response) => {
        setRecommendedAnime(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  }

  async function fetchLikedAnimeId() {
    await axios
      .post("http://127.0.0.1:8000/api/like_anime/", {
        name: localStorage.getItem("email"),
      })
      .then((response) => {
        for (const x in response.data) {
          setLikedAnime((prev) => [...prev, response.data[x]["anime"]["id"]]);
        }
      })
      .catch((error) => {
        console.log(error);
      });
  }

  useEffect(() => {
    getFavouriteGenres();
    getRecommended();
    fetchLikedAnimeId();
  }, []);

  //This stuff is copied from recharts official site
  const renderActiveShape = (props: any) => {
    const RADIAN = Math.PI / 180;
    const {
      cx,
      cy,
      midAngle,
      innerRadius,
      outerRadius,
      startAngle,
      endAngle,
      fill,
      payload,
      percent,
      value,
    } = props;
    const sin = Math.sin(-RADIAN * midAngle);
    const cos = Math.cos(-RADIAN * midAngle);
    const sx = cx + (outerRadius + 10) * cos;
    const sy = cy + (outerRadius + 10) * sin;
    const mx = cx + (outerRadius + 30) * cos;
    const my = cy + (outerRadius + 30) * sin;
    const ex = mx + (cos >= 0 ? 1 : -1) * 22;
    const ey = my;
    const textAnchor = cos >= 0 ? "start" : "end";

    return (
      <g>
        <text x={cx} y={cy} dy={8} textAnchor="middle" fill={fill}>
          {payload.name}
        </text>
        <Sector
          cx={cx}
          cy={cy}
          innerRadius={innerRadius}
          outerRadius={outerRadius}
          startAngle={startAngle}
          endAngle={endAngle}
          fill={fill}
        />
        <Sector
          cx={cx}
          cy={cy}
          startAngle={startAngle}
          endAngle={endAngle}
          innerRadius={outerRadius + 6}
          outerRadius={outerRadius + 10}
          fill={fill}
        />
        <path
          d={`M${sx},${sy}L${mx},${my}L${ex},${ey}`}
          stroke={fill}
          fill="none"
        />
        <circle cx={ex} cy={ey} r={2} fill={fill} stroke="none" />
        <text
          x={ex + (cos >= 0 ? 1 : -1) * 12}
          y={ey}
          textAnchor={textAnchor}
          fill="#333"
        >{`PV ${value}`}</text>
        <text
          x={ex + (cos >= 0 ? 1 : -1) * 12}
          y={ey}
          dy={18}
          textAnchor={textAnchor}
          fill="#999"
        >
          {`(Rate ${(percent * 100).toFixed(2)}%)`}
        </text>
      </g>
    );
  };

  const [activeIndex, setActiveIndex] = useState(0);
  const onPieEnter = useCallback(
    (_, index) => {
      setActiveIndex(index);
    },
    [setActiveIndex]
  );
  return (
    <div>
      <Navbar />
      <div className="ml-[20%] mt-[5%] text-xl">YOUR GENRE SPREAD</div>
      <div className="grid grid-cols-2 mt-[4%]">
        <div>
          <ResponsiveContainer minwidth={"100%"} height={300}>
            <PieChart width={800} height={1000}>
              <Pie
                activeIndex={activeIndex}
                activeShape={renderActiveShape}
                data={favouriteGenres}
                cx={500}
                cy={150}
                innerRadius={60}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
                onMouseEnter={onPieEnter}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="text-lg">
          <div className="mb-[2%]">YOUR FAVOURITE GENRES</div>
          <div>
            {favouriteGenres.slice(0, 7).map((genre, index) => {
              return (
                <>
                  <div className="mt-[0.5%] grid grid-cols-2">
                    <div>{genre["name"]}</div>
                    <div>{genre["value"]}</div>
                  </div>
                </>
              );
            })}
          </div>
        </div>
      </div>
        <div className="grid grid-cols-3 my-24">
          <div className="text-xl ml-[55%]">RECOMMMENDATIONS</div>
          <div></div>
          <div
            className="ml-[25%] cursor-pointer text-lg hover:underline"
            onClick={() => {
              showXAmount == 5 ? setXAmount(50) : setXAmount(5);
            }}
          >
            {showXAmount == 5 ? "Show more" : "Show Less"}
          </div>
        </div>
      {recommendedAnime[0] ? (
        <>
          <div className="pb-[5%]">
            <div className="mx-[20%] grid grid-cols-5 space-0">
              {range(0, showXAmount).map((index) => {
                const anime = recommendedAnime[index];
                const fav = likedAnime.includes(anime.id) ? true : false;
                return (
                  <div className="w-[80%] h-[100%]">
                    <AnimePanel
                      name={anime.name}
                      studios={anime.studios}
                      genres={anime.genres}
                      score={anime.score}
                      img={anime.img}
                      desc={anime.desc}
                      favourited={fav}
                    />
                  </div>
                );
              })}
            </div>
          </div>
        </>
      ) : null}
            {arrow ? 
                <FaArrowCircleUp onClick={scrollToTop} className="cursor-pointer fixed bottom-0 right-[12rem] content-center size-[3rem] m-[2%]"/>
            : null}
    </div>
  );
}

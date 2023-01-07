import React, {useState, useEffect} from 'react'

import Tweet from '../components/Tweet'

export default function Newsfeed() {
    const [posts, setPosts] = useState([])

    useEffect(() => {
        async function fetchData() {
            await fetch('/api/posts', {
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then((res) => res.json())
            .then((data) => setPosts(data))
        }

        fetchData()

        .catch(console.error)
    }, [])

    return(
        <>
            <div
                className="w3-container w3-jumbo"
                style={{ margin: "3rem", paddingLeft: "1rem" }}>
                Tweets
            </div>
            <div className="w3-container">
                {posts.map((item, index) => {
                    return (
                        <Tweet
                            title={item.title}
                            content={item.content}
                            key={index}
                        />
                    );
                })}
            </div>
        </>
    )
}
import React from 'react'

import Tweet from '../components/Tweet'

export default function Newsfeed() {
    const tweets = [
        {
            title: "Hello, world!",
            content: "<h3>Just gonna type html here!</h3>",
        },
        { title: "Tweet", content: "<code>Code!</code>" },
        {
            title: "Nice!",
            content:
                "<a href='https://www.youtube.com/watch?v=dQw4w9WgXcQ'>Here's a link! I need to use single quotes for the href.</a>",
        },
        {
            title: "Hello, world!",
            content:
                "<div>Typing <strong>using</strong> <em>more</em> <u>than</u> <sup>one</sup> <sub>html</sub> <del>tag</del>!</div>",
        },
    ]
    return(
        <>
            <div
                className="w3-container w3-jumbo"
                style={{ margin: "3rem", paddingLeft: "1rem" }}>
                Tweets
            </div>
            <div className="w3-container">
                {tweets.map((item, index) => {
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
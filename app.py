from flask import Flask, render_template, request
import spacy

# Initialize Flask app
app = Flask(__name__)

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Define FAQ data (This can be expanded with more questions and answers)
faq_data = {
    "What is the universe?": "The universe is the totality of space, time, matter, and energy that exists. It includes everything that is observable and beyond.",
    "How old is the universe?": "The universe is approximately 13.8 billion years old, according to scientific estimates.",
    "What is dark matter?": "Dark matter is a form of matter that does not emit light or energy, making it invisible to current scientific instruments. It is believed to make up most of the mass in the universe.",
    "What is a black hole?": "A black hole is a region of spacetime where gravity is so strong that not even light can escape from it. They are formed from collapsing stars.",
    "What is the Big Bang Theory?": "The Big Bang Theory posits that the universe began as a singularity about 13.8 billion years ago and has been expanding ever since.",
    "What is the observable universe?": "The observable universe refers to the part of the universe that we can observe and measure, limited by the speed of light and the age of the universe.",
    "What is the cosmic microwave background?": "The cosmic microwave background (CMB) is the faint glow of radiation left over from the Big Bang. It is a key piece of evidence for the Big Bang Theory.",
    "What is a galaxy?": "A galaxy is a massive system of stars, stellar remnants, interstellar gas, dust, and dark matter bound together by gravity. The Milky Way is the galaxy in which our solar system resides.",
    "What is the multiverse?": "The multiverse is a hypothetical set of multiple, potentially infinite, universes that exist parallel to each other, each with different physical properties and laws.",
    "What is dark energy?": "Dark energy is a mysterious form of energy that is causing the accelerated expansion of the universe. It is believed to make up about 68% of the universe's total energy content.",
    "What is the speed of light?": "The speed of light in a vacuum is approximately 299,792 kilometers per second (186,282 miles per second). It is the fastest known speed in the universe.",
    "What is a neutron star?": "A neutron star is the remnants of a massive star that has exploded in a supernova. It is an extremely dense object made almost entirely of neutrons.",
    "What is the event horizon?": "The event horizon is the boundary surrounding a black hole beyond which nothing, not even light, can escape due to the immense gravitational pull.",
    "What is a supernova?": "A supernova is a powerful explosion that occurs when a star reaches the end of its life cycle, releasing a massive amount of energy and often leaving behind a neutron star or black hole.",
    "What is the expansion of the universe?": "The expansion of the universe refers to the ongoing process of the universe growing in size, where galaxies are moving away from each other due to the stretching of space itself.",
    "What is a quasar?": "A quasar is an extremely bright and energetic center of a distant galaxy, powered by a supermassive black hole consuming large amounts of matter.",
    "What is gravitational lensing?": "Gravitational lensing occurs when the light from a distant object is bent around a massive object, such as a galaxy or black hole, due to the warping of spacetime caused by its gravity.",
    "What is a wormhole?": "A wormhole is a hypothetical tunnel-like structure that connects two separate points in spacetime, potentially allowing faster-than-light travel or shortcuts through the universe.",
    "What is the Hubble Space Telescope?": "The Hubble Space Telescope is a space-based observatory that has provided some of the most detailed images of distant galaxies, nebulae, and other cosmic phenomena.",
    "What is the theory of relativity?": "The theory of relativity, developed by Albert Einstein, describes the relationship between space, time, and gravity. It includes both the special and general theories of relativity.",
    "What is the Planck length?": "The Planck length is the smallest possible length scale in the universe, approximately 1.6 × 10^-35 meters, below which the laws of physics as we know them break down.",
    "What is a red giant?": "A red giant is a type of star that has exhausted the hydrogen in its core and expanded to a much larger size. These stars are at an advanced stage of stellar evolution.",
    "What is the Big Crunch?": "The Big Crunch is a theoretical scenario where the universe's expansion eventually slows down and reverses, leading to all matter collapsing back into a singularity.",
    "What is the cosmological constant?": "The cosmological constant, denoted by Lambda (Λ), is a term in Einstein's equations of general relativity that represents a constant energy density filling space homogeneously, associated with dark energy.",
    "What is a comet?": "A comet is a small celestial body made of ice, dust, and rocky material. When it passes close to the Sun, it heats up and releases gas and dust, forming a visible tail.",
    "What is the solar system?": "The solar system consists of the Sun and all the celestial objects that are gravitationally bound to it, including eight planets, their moons, asteroids, and comets.",
    "What is a galaxy cluster?": "A galaxy cluster is a large group of galaxies that are bound together by gravity. Clusters can contain hundreds to thousands of galaxies.",
    "What is antimatter?": "Antimatter consists of particles that are the opposite of ordinary matter. For example, the antiparticle of an electron is called a positron, with a positive charge instead of a negative one.",
    "What is the Fermi Paradox?": "The Fermi Paradox refers to the apparent contradiction between the high probability of extraterrestrial life in the universe and the lack of evidence or contact with such civilizations.",
    "What is the universe made of?": "The universe is made up of matter, energy, space, and time. It includes everything we can see, as well as things we can't, like dark matter and dark energy.",
    "What is a star?": "A star is a massive ball of gas, mostly hydrogen and helium, that emits light and heat due to nuclear reactions occurring in its core.",
    "What is the moon?": "The Moon is Earth's only natural satellite, orbiting our planet. It is a rocky, airless world that affects tides on Earth.",
    "What is a planet?": "A planet is a large celestial body that orbits a star. Planets do not produce their own light but reflect the light of their star.",
    "What is the Milky Way?": "The Milky Way is the galaxy that contains our solar system. It is a spiral galaxy with billions of stars, including our Sun.",
    "What is a solar eclipse?": "A solar eclipse happens when the Moon passes between the Earth and the Sun, blocking the Sun's light and casting a shadow on Earth.",
    "What is a lunar eclipse?": "A lunar eclipse occurs when the Earth comes between the Sun and the Moon, causing Earth's shadow to fall on the Moon.",
    "What is gravity?": "Gravity is the force that attracts objects with mass towards one another. It keeps planets in orbit around stars and causes objects to fall to the ground on Earth.",
    "What is space?": "Space is the vast, seemingly empty expanse that exists beyond Earth's atmosphere. It contains stars, planets, galaxies, and other celestial objects.",
    "What is an asteroid?": "An asteroid is a small rocky object that orbits the Sun, mostly found in the asteroid belt between Mars and Jupiter.",
    "What is a nebula?": "A nebula is a cloud of gas and dust in space, often the birthplace of stars. Some nebulae are visible to the naked eye, appearing as faint, colorful patches.",
    "What happened during the Big Bang?": "During the Big Bang, the universe began to expand from a very hot and dense state. In the first few moments, particles like protons, neutrons, and electrons formed, and as the universe cooled, atoms, stars, and galaxies formed.",
    "What is cosmic inflation?": "Cosmic inflation is a theory that proposes that in the first tiny fraction of a second after the Big Bang, the universe expanded exponentially at an incredible rate, far faster than the speed of light.",
    "What is the origin of the universe?": "The origin of the universe, according to the Big Bang Theory, is the moment when all of space, time, matter, and energy were contained in a singularity and rapidly expanded, creating the universe as we know it.",
    "What is a singularity?": "A singularity is a point in space where the gravitational forces are so intense that spacetime becomes infinitely curved, and physical laws break down. It is thought to exist at the center of black holes and at the beginning of the universe.",
    "What is the cosmic microwave background radiation?": "The cosmic microwave background (CMB) radiation is the faint glow left over from the Big Bang. It provides a snapshot of the early universe and serves as key evidence for the Big Bang Theory.",
    "How do scientists measure the age of the universe?": "Scientists estimate the age of the universe by studying the cosmic microwave background radiation and observing the oldest stars, galaxies, and the rate of expansion of the universe, known as the Hubble constant.",
    "What is dark matter and how does it relate to the Big Bang?": "Dark matter is a mysterious form of matter that doesn't emit light or energy, but it exerts gravitational influence. It is thought to have played a key role in the formation of galaxies after the Big Bang.",
    "What is the role of gravity in the universe?": "Gravity is the fundamental force that governs the movement of planets, stars, galaxies, and even light. It is the force that keeps objects in orbit and governs the structure of the universe.",
}


# Define function to get the best matching FAQ answer
def get_answer(question):
    doc = nlp(question)
    best_match = None
    highest_similarity = 0.0

    for faq_question, answer in faq_data.items():
        faq_doc = nlp(faq_question)
        similarity = doc.similarity(faq_doc)
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = answer

    return best_match or "Sorry, I don't have an answer to that question."


# Define routes for the app
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.form["question"]
    answer = get_answer(user_question)
    return render_template("index.html", question=user_question, answer=answer)


if __name__ == "__main__":
    app.run(debug=True)

## Data Preparation

Before we can build a Retrieval-Augmented Generation (RAG) system, we need to get our data into shape. Think of this step like **preparing ingredients before cooking a meal**: if the vegetables are dirty, the spices are scattered, and the meat is uncut, your final dish won’t turn out well. In RAG, data preparation ensures the model has **clean, organized, and properly portioned information** to work with.

---

### Collecting & Cleaning Documents

The first step is gathering all the text you want your system to “know.” This could include:

- Research papers
- Company manuals
- Policies and procedures
- Blogs, FAQs, or customer support documents

But raw documents are messy. They often contain:

- Page numbers, headers, footers
- Repeated disclaimers
- Formatting errors
- Random symbols

Cleaning means stripping out all the unnecessary parts and keeping only what’s useful. If you’re making lemonade, you don’t just throw in the whole lemon. You cut it, squeeze out the juice, leave behind the peel and seeds… and only then, if you’re feeling wild, turn it into a coronarita.

---

### Chunking Strategies

LLMs can’t handle huge documents in one go, so we need to break text into **bite-sized chunks**. There are many ways to do this, but in this course, we’ll focus only on the techniques that have **proven effective in real-world RAG pipelines**.

Here’s what works well:

1. **Fixed-size chunks** – Split the text every *N* words or tokens.

   - **Why it works**: Simple, fast, and easy to implement.
   - **Caution**: May cut off sentences or ideas mid-way, so context can sometimes get lost.
2. **Semantic chunks** – Split text by paragraphs, sections, or headings to preserve meaning.

   - **Why it works**: Keeps ideas intact, so retrieved chunks are self-contained and understandable.
   - **Pro tip**: Great for manuals, research papers, or any structured document.
3. **Hybrid approach** – Combine fixed-size and semantic splitting.

   - **Why it works**: Balances speed and readability, preventing chunks from being too small or too large.

By sticking to these approaches, you’ll get **chunks that are meaningful, manageable, and ready for your RAG retriever**.

---

### Preprocessing Text

After chunking, the text needs to be polished so it’s **consistent, clean, and machine-friendly**. Preprocessing ensures that the model can read and understand the chunks effectively. Common steps include:

- **Expanding acronyms**: Convert domain-specific abbreviations (e.g., ICU translates to "Intensive Care Unit" in medical domain but not "I See You".) so the model understands them.
- **Adding missing context**: Include any small but important details that were lost during chunking or extraction.
- **Handling punctuation, special symbols, or extra spaces**: Clean up stray characters that could confuse the model.
- **Converting tables, lists, or structured data into readable formats**: Make sure the model can interpret them correctly without losing meaning.

Think of this as cleaning and arranging your kitchen before cooking. You don’t want onion peels in your salad or mismatched measuring spoons. A neat setup means smoother cooking — and smoother retrieval for RAG.

---

Data preparation ensures your RAG pipeline doesn’t trip over messy, oversized, or inconsistent data. It’s the difference between serving a Michelin-star meal and handing someone raw flour and eggs.

# 🤖 AI Integration Guide - Where to Add AI Features

This guide shows **exactly where** in your codebase you can integrate different AI features for **The Queens** e-commerce store.

## 🎯 Current AI Integration

**✅ Already Implemented:**
- **AI Chatbot** - Located in `frontend/src/components/Chatbot.js` and `backend_django/api/views.py` (chatbot endpoint)

---

## 1. 🎯 AI Product Recommendations

### **Where to Add:**

#### **Backend:** `backend_django/api/views.py`
**Add after line 200 (after OrderViewSet):**

```python
@api_view(['GET'])
@permission_classes([AllowAny])
def get_recommendations(request, product_id):
    """Get AI-powered product recommendations"""
    try:
        product = Product.objects.get(id=product_id)
        
        # Simple AI: Find similar products by category
        similar_products = Product.objects.filter(
            category=product.category
        ).exclude(id=product_id)[:5]
        
        # Advanced AI: Use ML model for recommendations
        # recommendations = ml_model.recommend(product_id, top_n=5)
        
        serializer = ProductSerializer(similar_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
```

#### **Backend URLs:** `backend_django/api/urls.py`
**Add to urlpatterns (around line 18):**
```python
path('products/<int:product_id>/recommendations/', get_recommendations, name='recommendations'),
```

#### **Frontend:** `frontend/src/pages/ProductDetail.js`
**Add after line 148 (after product info div):**

```javascript
const [recommendations, setRecommendations] = useState([]);

useEffect(() => {
  // Fetch recommendations when product loads
  const fetchRecommendations = async () => {
    try {
      const response = await axios.get(
        `http://localhost:8000/api/products/${id}/recommendations/`
      );
      setRecommendations(response.data);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    }
  };
  if (product) {
    fetchRecommendations();
  }
}, [id, product]);

// Add to JSX after line 149 (after product-detail-content closing div):
{recommendations.length > 0 && (
  <div className="recommendations-section">
    <h2>You May Also Like</h2>
    <div className="recommendations-grid">
      {recommendations.map((item) => (
        <Link key={item.id} to={`/products/${item.id}`} className="recommendation-card">
          <img src={item.image_url} alt={item.name} />
          <h3>{item.name}</h3>
          <p>€{item.price.toFixed(2)}</p>
        </Link>
      ))}
    </div>
  </div>
)}
```

---

## 2. 🔍 Intelligent Search with AI

### **Where to Add:**

#### **Backend:** `backend_django/api/views.py`
**Modify existing `ProductViewSet` (around line 50-80):**

```python
def get_queryset(self):
    queryset = Product.objects.all()
    search = self.request.query_params.get('search', None)
    
    if search:
        # Current simple search
        # queryset = queryset.filter(name__icontains=search)
        
        # AI-Enhanced Search with fuzzy matching
        from difflib import SequenceMatcher
        
        def similarity_score(product_name, query):
            return SequenceMatcher(None, product_name.lower(), query.lower()).ratio()
        
        # Get all products with similarity scores
        products_with_scores = [
            (p, similarity_score(p.name, search)) for p in queryset
        ]
        
        # Filter products with >30% similarity
        products_with_scores = [(p, score) for p, score in products_with_scores if score > 0.3]
        
        # Sort by similarity score
        products_with_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Return product IDs
        product_ids = [p.id for p, _ in products_with_scores[:20]]
        queryset = Product.objects.filter(id__in=product_ids)
    
    return queryset
```

#### **Frontend:** `frontend/src/pages/Products.js`
**Add autocomplete feature (after line 104):**

```javascript
const [searchSuggestions, setSearchSuggestions] = useState([]);

useEffect(() => {
  // Debounced search suggestions
  const timer = setTimeout(() => {
    if (search.length > 2) {
      fetchSearchSuggestions(search);
    } else {
      setSearchSuggestions([]);
    }
  }, 300);

  return () => clearTimeout(timer);
}, [search]);

const fetchSearchSuggestions = async (query) => {
  try {
    const response = await axios.get('http://localhost:8000/api/products/', {
      params: { search: query }
    });
    setSearchSuggestions(response.data.results?.slice(0, 5) || []);
  } catch (error) {
    console.error('Error fetching suggestions:', error);
  }
};

// Modify search input (around line 98-104):
<div className="search-box">
  <input
    type="text"
    placeholder="Search products..."
    value={search}
    onChange={(e) => setSearch(e.target.value)}
    className="search-input"
    onFocus={() => setShowSuggestions(true)}
    onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
  />
  {searchSuggestions.length > 0 && (
    <div className="search-suggestions">
      {searchSuggestions.map((product) => (
        <Link
          key={product.id}
          to={`/products/${product.id}`}
          className="suggestion-item"
        >
          {product.name} - €{product.price}
        </Link>
      ))}
    </div>
  )}
</div>
```

---

## 3. 📸 Visual Product Search (Image Search)

### **Where to Add:**

#### **Backend:** `backend_django/api/views.py`
**Add after chatbot endpoint (around line 295):**

```python
@api_view(['POST'])
@permission_classes([AllowAny])
def visual_search(request):
    """AI-powered visual product search"""
    import base64
    from PIL import Image
    import io
    
    try:
        # Get uploaded image
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Option 1: Use Google Cloud Vision API (requires API key)
        # from google.cloud import vision
        # client = vision.ImageAnnotatorClient()
        # content = image_file.read()
        # image = vision.Image(content=content)
        # response = client.label_detection(image=image)
        # labels = [label.description for label in response.label_annotations]
        
        # Option 2: Simple color/pattern matching
        # Open image and extract dominant colors
        img = Image.open(image_file)
        img = img.convert('RGB')
        
        # Find products with similar category based on image analysis
        # This is a simplified version - real implementation would use ML
        
        # For now, return all products (you'd replace this with actual visual matching)
        products = Product.objects.all()[:10]
        serializer = ProductSerializer(products, many=True)
        
        return Response({
            'matches': serializer.data,
            'detected_labels': []  # Would contain AI-detected labels
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
```

#### **Backend URLs:** `backend_django/api/urls.py`
```python
path('products/visual-search/', visual_search, name='visual_search'),
```

#### **Frontend:** `frontend/src/pages/Products.js`
**Add camera/upload button (around line 97-104):**

```javascript
const [showImageUpload, setShowImageUpload] = useState(false);

const handleImageSearch = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append('image', file);

  try {
    const response = await axios.post(
      'http://localhost:8000/api/products/visual-search/',
      formData,
      { headers: { 'Content-Type': 'multipart/form-data' } }
    );
    setProducts(response.data.matches);
    setSearch(''); // Clear text search
  } catch (error) {
    console.error('Error with image search:', error);
  }
};

// Add to JSX (around line 96):
<div className="filters">
  <div className="search-box">
    <input
      type="text"
      placeholder="Search products..."
      value={search}
      onChange={(e) => setSearch(e.target.value)}
      className="search-input"
    />
    <label className="image-search-btn" title="Search by image">
      📷
      <input
        type="file"
        accept="image/*"
        onChange={handleImageSearch}
        style={{ display: 'none' }}
      />
    </label>
  </div>
  ...
</div>
```

---

## 4. ✍️ AI-Generated Product Descriptions

### **Where to Add:**

#### **Backend:** `backend_django/api/views.py`
**Add after visual_search (around line 330):**

```python
@api_view(['POST'])
@permission_classes([AllowAny])  # Or restrict to admin
def generate_description(request, product_id):
    """Generate AI-powered product description"""
    import os
    
    try:
        product = Product.objects.get(id=product_id)
        groq_api_key = os.environ.get('GROQ_API_KEY')
        
        if not groq_api_key:
            return Response(
                {'error': 'AI service not configured'}, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        from groq import Groq
        client = Groq(api_key=groq_api_key)
        
        prompt = f"""Write a compelling, SEO-friendly product description for:
Name: {product.name}
Category: {product.category}
Price: €{product.price}

Make it engaging, highlight key features, and keep it under 200 words."""
        
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            max_tokens=300,
            temperature=0.7
        )
        
        generated_description = response.choices[0].message.content.strip()
        
        # Update product description
        product.description = generated_description
        product.save()
        
        return Response({
            'description': generated_description,
            'message': 'Description generated successfully'
        }, status=status.HTTP_200_OK)
        
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
```

#### **Backend URLs:** `backend_django/api/urls.py`
```python
path('products/<int:product_id>/generate-description/', generate_description, name='generate_description'),
```

#### **Frontend:** `frontend/src/pages/ProductDetail.js`
**Add generate button (if admin) around line 106:**

```javascript
const [isGenerating, setIsGenerating] = useState(false);

const handleGenerateDescription = async () => {
  setIsGenerating(true);
  try {
    const response = await axios.post(
      `http://localhost:8000/api/products/${id}/generate-description/`
    );
    setProduct(prev => ({ ...prev, description: response.data.description }));
    alert('Description generated successfully!');
  } catch (error) {
    alert('Failed to generate description: ' + (error.response?.data?.error || error.message));
  } finally {
    setIsGenerating(false);
  }
};

// Add to JSX (around line 106):
<p className="product-detail-description">
  {product.description}
  {user?.is_staff && (
    <button 
      onClick={handleGenerateDescription}
      disabled={isGenerating}
      className="generate-btn"
    >
      {isGenerating ? 'Generating...' : '✨ Generate AI Description'}
    </button>
  )}
</p>
```

---

## 5. 😊 Review Sentiment Analysis

### **Where to Add:**

#### **Backend Models:** `backend_django/api/models.py`
**Add Review model (after OrderItem model):**

```python
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    sentiment_score = models.FloatField(null=True, blank=True)  # AI-generated
    sentiment_label = models.CharField(max_length=20, null=True, blank=True)  # positive/negative/neutral
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username if self.user else 'Guest'}"
```

#### **Backend Views:** `backend_django/api/views.py`
**Add sentiment analysis endpoint:**

```python
@api_view(['POST'])
@permission_classes([AllowAny])
def create_review(request, product_id):
    """Create review with AI sentiment analysis"""
    try:
        product = Product.objects.get(id=product_id)
        from textblob import TextBlob
        
        review_data = request.data
        comment = review_data.get('comment', '')
        
        # AI Sentiment Analysis using TextBlob
        blob = TextBlob(comment)
        sentiment_score = blob.sentiment.polarity  # -1 to 1
        sentiment_label = 'positive' if sentiment_score > 0.1 else 'negative' if sentiment_score < -0.1 else 'neutral'
        
        review = Review.objects.create(
            product=product,
            user=request.user if request.user.is_authenticated else None,
            rating=review_data.get('rating', 5),
            comment=comment,
            sentiment_score=sentiment_score,
            sentiment_label=sentiment_label
        )
        
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_product_sentiment(request, product_id):
    """Get overall sentiment analysis for a product"""
    try:
        reviews = Review.objects.filter(product_id=product_id)
        
        if not reviews.exists():
            return Response({'message': 'No reviews yet'}, status=status.HTTP_200_OK)
        
        # Calculate average sentiment
        avg_sentiment = sum(r.sentiment_score for r in reviews) / reviews.count()
        
        positive_count = reviews.filter(sentiment_label='positive').count()
        negative_count = reviews.filter(sentiment_label='negative').count()
        neutral_count = reviews.filter(sentiment_label='neutral').count()
        
        return Response({
            'average_sentiment': avg_sentiment,
            'sentiment_label': 'positive' if avg_sentiment > 0.1 else 'negative' if avg_sentiment < -0.1 else 'neutral',
            'positive_reviews': positive_count,
            'negative_reviews': negative_count,
            'neutral_reviews': neutral_count,
            'total_reviews': reviews.count()
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
```

#### **Backend Requirements:** `backend_django/requirements.txt`
```txt
textblob==0.17.1
```

#### **Frontend:** `frontend/src/pages/ProductDetail.js`
**Add reviews section (after line 149):**

```javascript
const [reviews, setReviews] = useState([]);
const [sentiment, setSentiment] = useState(null);

useEffect(() => {
  // Fetch reviews and sentiment
  const fetchReviews = async () => {
    try {
      const reviewsRes = await axios.get(
        `http://localhost:8000/api/products/${id}/reviews/`
      );
      setReviews(reviewsRes.data);
      
      const sentimentRes = await axios.get(
        `http://localhost:8000/api/products/${id}/sentiment/`
      );
      setSentiment(sentimentRes.data);
    } catch (error) {
      console.error('Error fetching reviews:', error);
    }
  };
  if (product) {
    fetchReviews();
  }
}, [id, product]);

// Add to JSX (after product-detail-content):
<div className="reviews-section">
  <h2>Customer Reviews</h2>
  {sentiment && (
    <div className="sentiment-summary">
      <span className={`sentiment-badge ${sentiment.sentiment_label}`}>
        {sentiment.sentiment_label === 'positive' ? '😊' : 
         sentiment.sentiment_label === 'negative' ? '😞' : '😐'} 
        {sentiment.sentiment_label} ({sentiment.total_reviews} reviews)
      </span>
    </div>
  )}
  <div className="reviews-list">
    {reviews.map((review) => (
      <div key={review.id} className="review-card">
        <div className="review-header">
          <strong>{review.user?.username || 'Guest'}</strong>
          <span className={`sentiment-${review.sentiment_label}`}>
            {review.sentiment_label}
          </span>
        </div>
        <div className="review-rating">⭐ {review.rating}/5</div>
        <p>{review.comment}</p>
      </div>
    ))}
  </div>
</div>
```

---

## 6. 🎯 Personalized Homepage

### **Where to Add:**

#### **Frontend:** `frontend/src/pages/Home.js`
**Modify to show personalized content:**

```javascript
import { useContext, useEffect, useState } from 'react';
import { AuthContext } from '../context/AuthContext';
import axios from 'axios';

const Home = () => {
  const { user } = useContext(AuthContext);
  const [personalizedProducts, setPersonalizedProducts] = useState([]);
  const [recommendations, setRecommendations] = useState([]);

  useEffect(() => {
    if (user) {
      // Fetch personalized recommendations
      fetchPersonalizedContent();
    } else {
      // Show popular products for guests
      fetchPopularProducts();
    }
  }, [user]);

  const fetchPersonalizedContent = async () => {
    try {
      // Get user's order history
      const ordersRes = await axios.get('http://localhost:8000/api/orders/');
      
      // Extract categories from previous orders
      const categories = new Set();
      ordersRes.data.forEach(order => {
        order.items?.forEach(item => {
          if (item.product?.category) {
            categories.add(item.product.category);
          }
        });
      });
      
      // Get products in user's preferred categories
      const productsRes = await axios.get('http://localhost:8000/api/products/', {
        params: { category: Array.from(categories)[0] }
      });
      
      setPersonalizedProducts(productsRes.data.results?.slice(0, 6) || []);
      
      // Get AI recommendations based on browsing/purchase history
      const recommendationsRes = await axios.get(
        `http://localhost:8000/api/users/${user.id}/recommendations/`
      );
      setRecommendations(recommendationsRes.data);
    } catch (error) {
      console.error('Error fetching personalized content:', error);
    }
  };

  const fetchPopularProducts = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/products/', {
        params: { ordering: '-created_at' }
      });
      setPersonalizedProducts(response.data.results?.slice(0, 6) || []);
    } catch (error) {
      console.error('Error fetching popular products:', error);
    }
  };

  return (
    <div className="home">
      {/* Existing hero section */}
      <section className="hero">...</section>

      {/* Personalized Section */}
      <section className="personalized-section">
        <div className="container">
          <h2 className="section-title">
            {user ? '✨ Recommended For You' : '🔥 Popular Products'}
          </h2>
          <div className="products-grid">
            {personalizedProducts.map((product) => (
              <div key={product.id} className="product-card">
                {/* Product card content */}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Existing features section */}
      <section className="features">...</section>
    </div>
  );
};
```

---

## 7. 💰 AI Price Optimization

### **Where to Add:**

#### **Backend:** `backend_django/api/views.py`
**Add admin endpoint:**

```python
@api_view(['POST'])
@permission_classes([IsAdminUser])
def optimize_price(request, product_id):
    """AI-powered price optimization suggestion"""
    try:
        product = Product.objects.get(id=product_id)
        
        # Analyze competitor prices, demand, inventory
        # This is a simplified version
        
        # Get similar products
        similar = Product.objects.filter(category=product.category).exclude(id=product_id)
        avg_price = similar.aggregate(avg=Avg('price'))['avg'] or product.price
        
        # AI logic (simplified)
        suggested_price = avg_price * 0.95  # 5% below average to be competitive
        
        # Check inventory
        if product.stock < 5:
            suggested_price *= 1.1  # Increase price if low stock
        
        return Response({
            'current_price': product.price,
            'suggested_price': round(suggested_price, 2),
            'recommendation': 'increase' if suggested_price > product.price else 'decrease',
            'reasoning': 'Based on competitor analysis and inventory levels'
        }, status=status.HTTP_200_OK)
        
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
```

---

## 📋 Quick Integration Checklist

### ✅ **Easy to Implement (Start Here):**
1. **Product Recommendations** - Simple category-based → 30 minutes
2. **Enhanced Search** - Fuzzy matching → 1 hour
3. **Review Sentiment** - TextBlob library → 2 hours

### ⭐ **High Impact:**
1. **AI-Generated Descriptions** - Uses existing Groq API → 1 hour
2. **Personalized Homepage** - Based on user history → 2 hours
3. **Visual Search** - Image upload feature → 3 hours

### 🚀 **Advanced Features:**
1. **Price Optimization** - ML-based pricing → 4+ hours
2. **Inventory Prediction** - Time series forecasting → 6+ hours

---

## 🔧 Installation Steps

### For Sentiment Analysis:
```bash
cd backend_django
source venv/bin/activate
pip install textblob
python -m textblob.download_corpora  # Download language data
```

### For Image Processing:
```bash
pip install Pillow  # Already installed
pip install google-cloud-vision  # For advanced image search (optional)
```

---

## 📍 File Structure Summary

```
backend_django/
├── api/
│   ├── models.py          # Add Review model here
│   ├── views.py           # Add all AI endpoints here
│   ├── urls.py            # Add new URL routes here
│   └── serializers.py     # Add ReviewSerializer

frontend/src/
├── pages/
│   ├── Products.js        # Add search suggestions, image search
│   ├── ProductDetail.js   # Add recommendations, reviews, sentiment
│   └── Home.js            # Add personalized content
├── components/
│   └── Chatbot.js         # ✅ Already has AI
```

---

## 🎯 Recommended Order of Implementation

1. **Week 1:** Product Recommendations + Enhanced Search
2. **Week 2:** Review Sentiment Analysis + AI Descriptions
3. **Week 3:** Personalized Homepage
4. **Week 4:** Visual Search (if needed)

---

**Which AI feature would you like me to implement first?** I recommend starting with **Product Recommendations** as it's the easiest and has immediate impact on sales! 🚀


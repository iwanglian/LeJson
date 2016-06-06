// Generated by LeJson ,  DO NOT EDIT!
// Feedback to https://github.com/iwanglian/LeJson/issues,  DO NOT EDIT!

// Created by alick on 2016-06-02 15:41:00,  DO NOT EDIT!

package com.github.iwanglian.lejson.model;

import java.util.List;
import com.alibaba.fastjson.annotation.JSONField;

public class FJTestModel {
	@JSONField(name = "date")
	private String date; 
	@JSONField(name = "top_stories")
	private List<TopStories> topStories; 
	@JSONField(name = "stories")
	private List<Stories> stories; 

    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    } 

    public List<TopStories> getTopStories() {
        return topStories;
    }

    public void setTopStories(List<TopStories> topStories) {
        this.topStories = topStories;
    } 

    public List<Stories> getStories() {
        return stories;
    }

    public void setStories(List<Stories> stories) {
        this.stories = stories;
    } 

	public static class TopStories {
		@JSONField(name = "image")
		private String image; 
		@JSONField(name = "type")
		private int type; 
		@JSONField(name = "id")
		private int id; 
		@JSONField(name = "ga_prefix")
		private String gaPrefix; 
		@JSONField(name = "title")
		private String title; 
	
	    public String getImage() {
	        return image;
	    }
	
	    public void setImage(String image) {
	        this.image = image;
	    } 
	
	    public int getType() {
	        return type;
	    }
	
	    public void setType(int type) {
	        this.type = type;
	    } 
	
	    public int getId() {
	        return id;
	    }
	
	    public void setId(int id) {
	        this.id = id;
	    } 
	
	    public String getGaPrefix() {
	        return gaPrefix;
	    }
	
	    public void setGaPrefix(String gaPrefix) {
	        this.gaPrefix = gaPrefix;
	    } 
	
	    public String getTitle() {
	        return title;
	    }
	
	    public void setTitle(String title) {
	        this.title = title;
	    } 
	}
	

	public static class Stories {
		@JSONField(name = "images")
		private List<String> images; 
		@JSONField(name = "type")
		private int type; 
		@JSONField(name = "id")
		private int id; 
		@JSONField(name = "ga_prefix")
		private String gaPrefix; 
		@JSONField(name = "title")
		private String title; 
	
	    public List<String> getImages() {
	        return images;
	    }
	
	    public void setImages(List<String> images) {
	        this.images = images;
	    } 
	
	    public int getType() {
	        return type;
	    }
	
	    public void setType(int type) {
	        this.type = type;
	    } 
	
	    public int getId() {
	        return id;
	    }
	
	    public void setId(int id) {
	        this.id = id;
	    } 
	
	    public String getGaPrefix() {
	        return gaPrefix;
	    }
	
	    public void setGaPrefix(String gaPrefix) {
	        this.gaPrefix = gaPrefix;
	    } 
	
	    public String getTitle() {
	        return title;
	    }
	
	    public void setTitle(String title) {
	        this.title = title;
	    } 
	}
	
}


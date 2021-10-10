module github.com/crawlab-team/plugin-scrapy

go 1.15

replace github.com/crawlab-team/crawlab-core => /Users/marvzhang/projects/crawlab-team/crawlab-core

require (
	github.com/crawlab-team/crawlab-core v0.6.0-beta.20211009.1458
	github.com/crawlab-team/crawlab-plugin v0.6.0-beta.20211009.1505
	github.com/crawlab-team/go-trace v0.1.0
	github.com/gin-gonic/gin v1.7.4
	github.com/go-python/gpython v0.0.3
	github.com/spf13/viper v1.9.0
	go.mongodb.org/mongo-driver v1.7.3
)

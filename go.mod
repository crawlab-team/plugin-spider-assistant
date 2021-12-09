module github.com/crawlab-team/plugin-scrapy

go 1.16

replace (
	github.com/crawlab-team/crawlab-core => ../crawlab-core
	github.com/crawlab-team/crawlab-plugin => ../crawlab-plugin
)

require (
	github.com/crawlab-team/crawlab-core v0.6.0-beta.20211009.1458
	github.com/crawlab-team/crawlab-plugin v0.6.0-beta.20211009.1505
	github.com/crawlab-team/go-trace v0.1.0
	github.com/gin-gonic/gin v1.7.4
	go.mongodb.org/mongo-driver v1.8.0
)

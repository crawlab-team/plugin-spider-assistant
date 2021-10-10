package services

import (
	"errors"
	"github.com/crawlab-team/crawlab-core/controllers"
	"github.com/crawlab-team/crawlab-core/interfaces"
	"github.com/crawlab-team/crawlab-core/spider/fs"
	"github.com/crawlab-team/crawlab-core/utils"
	"github.com/crawlab-team/go-trace"
	"github.com/crawlab-team/plugin-scrapy/constants"
	"github.com/crawlab-team/plugin-scrapy/entity"
	"github.com/gin-gonic/gin"
	"github.com/go-python/gpython/compile"
	"github.com/spf13/viper"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"io/ioutil"
	"os"
	"path"
	"strings"
)

type ScrapyService struct {
	parent *Service
	api    *gin.Engine
}

func (svc *ScrapyService) Init() {
	svc.api.GET("/scrapy/:id", svc.get)
}

func (svc *ScrapyService) get(c *gin.Context) {
	// spider id
	id, err := primitive.ObjectIDFromHex(c.Param("id"))
	if err != nil {
		controllers.HandleErrorBadRequest(c, err)
		return
	}

	//// spider
	//s, err := svc.parent.getSpider(id)
	//if err != nil {
	//	controllers.HandleErrorInternalServerError(c, err)
	//	return
	//}

	// spider fs service
	fsSvc, err := fs.NewSpiderFsService(id)
	if err != nil {
		controllers.HandleErrorInternalServerError(c, err)
		return
	}

	// sync to workspace
	if err := fsSvc.GetFsService().SyncToWorkspace(); err != nil {
		controllers.HandleErrorInternalServerError(c, err)
		return
	}

	// scrapy.cfg
	//cfg, err := svc._getScrapyCfg(fsSvc)
	//if err != nil {
	//	controllers.HandleErrorInternalServerError(c, err)
	//	return
	//}
	//controllers.HandleSuccessWithData(c, cfg)

	//filepath := path.Join(fsSvc.GetWorkspacePath(), "scrapy_baidu", "settings.py")
	//filepath := path.Join(fsSvc.GetWorkspacePath(), "scrapy_baidu", "spiders", "baidu.py")
	filepath := path.Join(fsSvc.GetWorkspacePath(), "scrapy_baidu", "items.py")
	py, err := svc._parsePy(filepath)
	if err != nil {
		controllers.HandleErrorInternalServerError(c, err)
		return
	}
	controllers.HandleSuccessWithData(c, py)
}

func (svc *ScrapyService) _getScrapyCfg(fsSvc interfaces.SpiderFsService) (cfg *entity.ScrapyCfg, err error) {
	// cfg path
	cfgPath := path.Join(fsSvc.GetWorkspacePath(), constants.ScrapyCfgFileName)
	if !utils.Exists(cfgPath) {
		return nil, errors.New("not exists")
	}

	// read cfg into viper config
	f, err := os.Open(cfgPath)
	if err != nil {
		return nil, trace.TraceError(err)
	}
	vp := viper.New()
	vp.SetConfigType("ini")
	if err := vp.ReadConfig(f); err != nil {
		return nil, trace.TraceError(err)
	}

	// cfg
	cfg = entity.NewScrapyCfg()

	// iterate viper keys
	for _, k := range vp.AllKeys() {
		v := vp.GetString(k)
		if strings.HasPrefix(k, "settings") {
			cfg.Settings[k] = v
		} else if strings.HasPrefix(k, "deploy") {
			cfg.Deploy[k] = v
		}
	}

	return cfg, nil
}

func (svc *ScrapyService) _parsePy(filepath string) (res interface{}, err error) {
	src, err := ioutil.ReadFile(filepath)
	if err != nil {
		return nil, err
	}
	return compile.Compile(string(src), filepath, "exec", 0, false)
}

func NewScrapyService(parent *Service) (svc *ScrapyService) {
	svc = &ScrapyService{
		parent: parent,
		api:    parent.GetApi(),
	}
	return svc
}
